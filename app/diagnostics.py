from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFrame,
    QFormLayout,
)

from app.core.battery import (
    calculate_soh,
    classify_health,
    calculate_capacity_degradation,
)

from app.core.rul import (
    estimate_rul_years,
    classify_rul,
)


class DiagnosticsView(QWidget):
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

            QLineEdit,
            QComboBox {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 9px;
                font-size: 13px;
            }

            QLineEdit:focus,
            QComboBox:focus {
                border: 1px solid #2563eb;
            }

            QPushButton#analyze_button {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 11px 20px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#analyze_button:hover {
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

            QLabel[role="result_status"] {
                font-size: 13px;
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

        title = QLabel("Battery Diagnostics")
        title.setProperty("role", "title")

        subtitle = QLabel(
            "Enter battery information to perform a health assessment."
        )
        subtitle.setProperty("role", "subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------------------------------------------------------
        # Battery Information Card
        # ---------------------------------------------------------

        battery_card = QFrame()
        battery_card.setProperty("role", "card")

        battery_layout = QVBoxLayout(battery_card)

        section_title = QLabel("Battery Information")
        section_title.setProperty("role", "section")

        battery_layout.addWidget(section_title)

        form = QFormLayout()
        form.setSpacing(12)

        self.chemistry = QComboBox()
        self.chemistry.addItems([
            "Lithium-ion (NMC)",
            "Lithium-ion (LFP)",
            "Lithium-ion (NCA)",
            "Other",
        ])

        self.rated_capacity = QLineEdit()
        self.rated_capacity.setPlaceholderText("e.g. 60")

        self.current_capacity = QLineEdit()
        self.current_capacity.setPlaceholderText("e.g. 52")

        self.voltage = QLineEdit()
        self.voltage.setPlaceholderText("e.g. 400")

        self.current = QLineEdit()
        self.current.setPlaceholderText("e.g. 120")

        self.temperature = QLineEdit()
        self.temperature.setPlaceholderText("e.g. 28")

        self.cycle_count = QLineEdit()
        self.cycle_count.setPlaceholderText("e.g. 842")

        # NEW: annual degradation rate
        self.annual_degradation = QLineEdit()
        self.annual_degradation.setPlaceholderText(
            "e.g. 2.8"
        )

        form.addRow(
            "Battery Chemistry:",
            self.chemistry,
        )

        form.addRow(
            "Rated Capacity (kWh):",
            self.rated_capacity,
        )

        form.addRow(
            "Current Capacity (kWh):",
            self.current_capacity,
        )

        form.addRow(
            "Pack Voltage (V):",
            self.voltage,
        )

        form.addRow(
            "Current (A):",
            self.current,
        )

        form.addRow(
            "Temperature (°C):",
            self.temperature,
        )

        form.addRow(
            "Cycle Count:",
            self.cycle_count,
        )

        form.addRow(
            "Annual Degradation (%/year):",
            self.annual_degradation,
        )

        battery_layout.addLayout(form)

        hint = QLabel(
            "Annual degradation is used by the prototype RUL model. "
            "It should come from historical battery data when available."
        )
        hint.setProperty("role", "hint")

        battery_layout.addWidget(hint)

        layout.addWidget(battery_card)

        # ---------------------------------------------------------
        # Assessment Result Card
        # ---------------------------------------------------------

        result_card = QFrame()
        result_card.setProperty("role", "card")

        result_layout = QHBoxLayout(result_card)

        # SoH
        soh_container = QVBoxLayout()

        soh_label = QLabel("STATE OF HEALTH")
        soh_label.setProperty("role", "result_label")

        self.soh_value = QLabel("--")
        self.soh_value.setProperty("role", "result_value")

        soh_container.addWidget(soh_label)
        soh_container.addWidget(self.soh_value)

        # Total degradation
        degradation_container = QVBoxLayout()

        degradation_label = QLabel(
            "CAPACITY LOSS"
        )
        degradation_label.setProperty(
            "role",
            "result_label",
        )

        self.degradation_value = QLabel("--")
        self.degradation_value.setProperty(
            "role",
            "result_value",
        )

        degradation_container.addWidget(
            degradation_label
        )

        degradation_container.addWidget(
            self.degradation_value
        )

        # Health status
        status_container = QVBoxLayout()

        status_label = QLabel(
            "HEALTH STATUS"
        )
        status_label.setProperty(
            "role",
            "result_label",
        )

        self.status_value = QLabel(
            "Awaiting assessment"
        )

        self.status_value.setProperty(
            "role",
            "result_status",
        )

        status_container.addWidget(
            status_label
        )

        status_container.addWidget(
            self.status_value
        )

        # RUL
        rul_container = QVBoxLayout()

        rul_label = QLabel(
            "ESTIMATED RUL"
        )
        rul_label.setProperty(
            "role",
            "result_label",
        )

        self.rul_value = QLabel("--")
        self.rul_value.setProperty(
            "role",
            "result_value",
        )

        rul_container.addWidget(
            rul_label
        )

        rul_container.addWidget(
            self.rul_value
        )

        result_layout.addLayout(
            soh_container
        )

        result_layout.addLayout(
            degradation_container
        )

        result_layout.addLayout(
            status_container
        )

        result_layout.addLayout(
            rul_container
        )

        layout.addWidget(result_card)

        # ---------------------------------------------------------
        # RUL explanation
        # ---------------------------------------------------------

        self.rul_status = QLabel("")
        self.rul_status.setProperty(
            "role",
            "hint",
        )

        layout.addWidget(
            self.rul_status
        )

        # ---------------------------------------------------------
        # Error message
        # ---------------------------------------------------------

        self.error_label = QLabel("")
        self.error_label.setProperty(
            "role",
            "error",
        )

        layout.addWidget(
            self.error_label
        )

        # ---------------------------------------------------------
        # Action Area
        # ---------------------------------------------------------

        action_row = QHBoxLayout()

        analyze_button = QPushButton(
            "Run Battery Assessment"
        )

        analyze_button.setObjectName(
            "analyze_button"
        )

        analyze_button.clicked.connect(
            self.run_assessment
        )

        action_row.addStretch()

        action_row.addWidget(
            analyze_button
        )

        layout.addLayout(
            action_row
        )

        layout.addStretch()

    def run_assessment(self):
        """
        Read the form and calculate:

        1. State of Health
        2. Total capacity loss
        3. Health classification
        4. Estimated RUL
        """

        self.error_label.setText("")
        self.rul_status.setText("")

        try:
            rated_capacity = float(
                self.rated_capacity.text()
            )

            current_capacity = float(
                self.current_capacity.text()
            )

            annual_degradation = float(
                self.annual_degradation.text()
            )

            # ---------------------------------------------
            # Battery health calculations
            # ---------------------------------------------

            soh = calculate_soh(
                rated_capacity,
                current_capacity,
            )

            capacity_loss = (
                calculate_capacity_degradation(
                    rated_capacity,
                    current_capacity,
                )
            )

            health_status = classify_health(
                soh
            )

            # ---------------------------------------------
            # RUL calculation
            # ---------------------------------------------

            rul_years = estimate_rul_years(
                current_soh=soh,
                annual_degradation_rate=annual_degradation,
            )

            rul_classification = classify_rul(
                rul_years
            )

            # ---------------------------------------------
            # Display results
            # ---------------------------------------------

            self.soh_value.setText(
                f"{soh:.1f}%"
            )

            self.degradation_value.setText(
                f"{capacity_loss:.1f}%"
            )

            self.status_value.setText(
                health_status
            )

            self.rul_value.setText(
                f"{rul_years:.1f} years"
            )

            self.rul_status.setText(
                f"RUL assessment: {rul_classification}"
            )

        except ValueError as error:

            self.soh_value.setText("--")
            self.degradation_value.setText("--")
            self.status_value.setText(
                "Assessment failed"
            )
            self.rul_value.setText("--")

            self.error_label.setText(
                f"Please enter valid values. {error}"
            )