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

from app.core.rul import estimate_rul_years, classify_rul


class RULAnalysisView(QWidget):
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

        title = QLabel("RUL Analysis")
        title.setProperty("role", "title")

        subtitle = QLabel(
            "Estimate remaining useful life using a simplified "
            "battery degradation model."
        )
        subtitle.setProperty("role", "subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------------------------------------------------------
        # Input Card
        # ---------------------------------------------------------

        input_card = QFrame()
        input_card.setProperty("role", "card")

        input_layout = QVBoxLayout(input_card)

        section_title = QLabel("RUL Parameters")
        section_title.setProperty("role", "section")

        input_layout.addWidget(section_title)

        form = QFormLayout()
        form.setSpacing(12)

        self.soh_input = QLineEdit()
        self.soh_input.setPlaceholderText("e.g. 86.7")

        self.degradation_input = QLineEdit()
        self.degradation_input.setPlaceholderText("e.g. 2.8")

        self.minimum_soh_input = QLineEdit()
        self.minimum_soh_input.setPlaceholderText("e.g. 70")

        form.addRow(
            "Current State of Health (%):",
            self.soh_input,
        )

        form.addRow(
            "Annual Degradation (%/year):",
            self.degradation_input,
        )

        form.addRow(
            "Minimum Useful SoH (%):",
            self.minimum_soh_input,
        )

        input_layout.addLayout(form)

        hint = QLabel(
            "The model assumes a simplified linear degradation rate."
        )
        hint.setProperty("role", "hint")

        input_layout.addWidget(hint)

        layout.addWidget(input_card)

        # ---------------------------------------------------------
        # Results Card
        # ---------------------------------------------------------

        result_card = QFrame()
        result_card.setProperty("role", "card")

        result_layout = QHBoxLayout(result_card)

        # RUL
        rul_container = QVBoxLayout()

        rul_label = QLabel("ESTIMATED RUL")
        rul_label.setProperty("role", "result_label")

        self.rul_value = QLabel("--")
        self.rul_value.setProperty("role", "result_value")

        rul_container.addWidget(rul_label)
        rul_container.addWidget(self.rul_value)

        # Classification
        status_container = QVBoxLayout()

        status_label = QLabel("RUL CLASSIFICATION")
        status_label.setProperty("role", "result_label")

        self.status_value = QLabel(
            "Awaiting analysis"
        )
        self.status_value.setProperty(
            "role",
            "status",
        )

        status_container.addWidget(status_label)
        status_container.addWidget(self.status_value)

        result_layout.addLayout(rul_container)
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
        # Action
        # ---------------------------------------------------------

        action_row = QHBoxLayout()

        calculate_button = QPushButton(
            "Calculate RUL"
        )

        calculate_button.setObjectName(
            "calculate_button"
        )

        calculate_button.clicked.connect(
            self.calculate_rul
        )

        action_row.addStretch()
        action_row.addWidget(
            calculate_button
        )

        layout.addLayout(action_row)

        layout.addStretch()

    def calculate_rul(self):
        """Calculate remaining useful life."""

        self.error_label.setText("")

        try:
            current_soh = float(
                self.soh_input.text()
            )

            annual_degradation = float(
                self.degradation_input.text()
            )

            minimum_soh = float(
                self.minimum_soh_input.text()
            )

            rul_years = estimate_rul_years(
                current_soh=current_soh,
                annual_degradation_rate=annual_degradation,
                minimum_soh=minimum_soh,
            )

            classification = classify_rul(
                rul_years
            )

            self.rul_value.setText(
                f"{rul_years:.1f} years"
            )

            self.status_value.setText(
                classification
            )

        except ValueError as error:

            self.rul_value.setText("--")

            self.status_value.setText(
                "Analysis failed"
            )

            self.error_label.setText(
                f"Please enter valid values. {error}"
            )