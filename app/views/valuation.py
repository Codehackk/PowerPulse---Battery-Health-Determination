from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QFormLayout,
)

from app.core.valuation import (
    calculate_residual_value,
    calculate_value_retention,
    classify_value_retention,
)


class ValuationView(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f7fb;
                color: #172033;
                font-family: "Segoe UI";
            }

            QLabel[role="title"] {
                font-size: 28px;
                font-weight: 700;
                color: #172033;
            }

            QLabel[role="subtitle"] {
                font-size: 14px;
                color: #64748b;
                padding-bottom: 14px;
            }

            QFrame[role="card"] {
                background-color: white;
                border: 1px solid #dfe5ee;
                border-radius: 12px;
            }

            QLabel[role="section"] {
                font-size: 16px;
                font-weight: 600;
                color: #172033;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 9px;
                font-size: 13px;
            }

            QLineEdit:focus {
                border: 1px solid #2563eb;
            }

            QPushButton#calculate_button {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 11px 20px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#calculate_button:hover {
                background-color: #1d4ed8;
            }

            QLabel[role="hint"] {
                color: #64748b;
                font-size: 12px;
            }

            QLabel[role="result_label"] {
                font-size: 11px;
                font-weight: 600;
                color: #64748b;
            }

            QLabel[role="result_value"] {
                font-size: 26px;
                font-weight: 700;
                color: #172033;
            }

            QLabel[role="status"] {
                font-size: 14px;
                font-weight: 600;
            }

            QLabel[role="error"] {
                color: #dc2626;
                font-size: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # ---------------------------------------------------------
        # Page heading
        # ---------------------------------------------------------

        title = QLabel("Battery Valuation")
        title.setProperty("role", "title")

        subtitle = QLabel(
            "Estimate the current residual value of a battery "
            "using health and remaining-life information."
        )
        subtitle.setProperty("role", "subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------------------------------------------------------
        # Input card
        # ---------------------------------------------------------

        input_card = QFrame()
        input_card.setProperty("role", "card")

        input_layout = QVBoxLayout(input_card)

        section_title = QLabel("Valuation Parameters")
        section_title.setProperty("role", "section")

        input_layout.addWidget(section_title)

        form = QFormLayout()
        form.setSpacing(12)

        self.original_value_input = QLineEdit()
        self.original_value_input.setPlaceholderText(
            "e.g. 1000000"
        )

        self.soh_input = QLineEdit()
        self.soh_input.setPlaceholderText(
            "e.g. 86.7"
        )

        self.rul_input = QLineEdit()
        self.rul_input.setPlaceholderText(
            "e.g. 6.0"
        )

        self.expected_life_input = QLineEdit()
        self.expected_life_input.setPlaceholderText(
            "e.g. 10"
        )

        form.addRow(
            "Original Battery Value (₹):",
            self.original_value_input,
        )

        form.addRow(
            "Current State of Health (%):",
            self.soh_input,
        )

        form.addRow(
            "Remaining Useful Life (years):",
            self.rul_input,
        )

        form.addRow(
            "Expected Battery Life (years):",
            self.expected_life_input,
        )

        input_layout.addLayout(form)

        hint = QLabel(
            "This is a simplified prototype valuation model. "
            "Research-backed valuation factors can be added later."
        )
        hint.setProperty("role", "hint")

        input_layout.addWidget(hint)

        layout.addWidget(input_card)

        # ---------------------------------------------------------
        # Results card
        # ---------------------------------------------------------

        result_card = QFrame()
        result_card.setProperty("role", "card")

        result_layout = QHBoxLayout(result_card)

        # Residual value
        value_container = QVBoxLayout()

        value_label = QLabel("ESTIMATED RESIDUAL VALUE")
        value_label.setProperty(
            "role",
            "result_label",
        )

        self.value_result = QLabel("--")
        self.value_result.setProperty(
            "role",
            "result_value",
        )

        value_container.addWidget(value_label)
        value_container.addWidget(self.value_result)

        # Value retention
        retention_container = QVBoxLayout()

        retention_label = QLabel("VALUE RETENTION")
        retention_label.setProperty(
            "role",
            "result_label",
        )

        self.retention_result = QLabel("--")
        self.retention_result.setProperty(
            "role",
            "result_value",
        )

        retention_container.addWidget(
            retention_label
        )
        retention_container.addWidget(
            self.retention_result
        )

        # Classification
        status_container = QVBoxLayout()

        status_label = QLabel("VALUATION STATUS")
        status_label.setProperty(
            "role",
            "result_label",
        )

        self.status_result = QLabel(
            "Awaiting analysis"
        )
        self.status_result.setProperty(
            "role",
            "status",
        )

        status_container.addWidget(status_label)
        status_container.addWidget(
            self.status_result
        )

        result_layout.addLayout(value_container)
        result_layout.addLayout(retention_container)
        result_layout.addLayout(status_container)

        layout.addWidget(result_card)

        # ---------------------------------------------------------
        # Error message
        # ---------------------------------------------------------

        self.error_label = QLabel("")
        self.error_label.setProperty(
            "role",
            "error",
        )

        layout.addWidget(self.error_label)

        # ---------------------------------------------------------
        # Calculate button
        # ---------------------------------------------------------

        action_row = QHBoxLayout()

        calculate_button = QPushButton(
            "Calculate Valuation"
        )

        calculate_button.setObjectName(
            "calculate_button"
        )

        calculate_button.clicked.connect(
            self.calculate_valuation
        )

        action_row.addStretch()
        action_row.addWidget(
            calculate_button
        )

        layout.addLayout(action_row)

        layout.addStretch()

    def calculate_valuation(self):
        """Calculate the estimated residual value."""

        self.error_label.setText("")

        try:
            original_value = float(
                self.original_value_input.text()
            )

            current_soh = float(
                self.soh_input.text()
            )

            current_rul_years = float(
                self.rul_input.text()
            )

            expected_life_years = float(
                self.expected_life_input.text()
            )

            residual_value = (
                calculate_residual_value(
                    original_value=original_value,
                    current_soh=current_soh,
                    current_rul_years=current_rul_years,
                    expected_life_years=expected_life_years,
                )
            )

            value_retention = (
                calculate_value_retention(
                    original_value=original_value,
                    residual_value=residual_value,
                )
            )

            classification = (
                classify_value_retention(
                    value_retention
                )
            )

            self.value_result.setText(
                f"₹{residual_value:,.2f}"
            )

            self.retention_result.setText(
                f"{value_retention:.2f}%"
            )

            self.status_result.setText(
                classification
            )

        except ValueError as error:

            self.value_result.setText("--")
            self.retention_result.setText("--")
            self.status_result.setText(
                "Analysis failed"
            )

            self.error_label.setText(
                f"Please enter valid values. {error}"
            )