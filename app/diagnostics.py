from PySide6.QtCore import Signal
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

    # ---------------------------------------------------------
    # Signal emitted when a battery assessment is completed.
    # MainWindow will use this to pass the result to Reports.
    # ---------------------------------------------------------

    analysis_completed = Signal(dict)

    def __init__(self):
        super().__init__()

        # -----------------------------------------------------
        # Shared analysis state
        # -----------------------------------------------------

        self.analysis_result = None

        # -----------------------------------------------------
        # Page styling
        # -----------------------------------------------------

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

            QLabel[role="field"] {
                font-size: 13px;
                color: #172033;
            }

            QLineEdit,
            QComboBox {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 9px;
                font-size: 13px;
                min-height: 18px;
            }

            QLineEdit:focus,
            QComboBox:focus {
                border: 1px solid #2563eb;
            }

            QComboBox {
                padding-left: 10px;
            }

            QPushButton#assessment_button {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 11px 20px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#assessment_button:hover {
                background-color: #1d4ed8;
            }

            QPushButton#assessment_button:pressed {
                background-color: #1e40af;
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
                font-size: 22px;
                font-weight: 700;
                color: #172033;
            }

            QLabel[role="status"] {
                font-size: 14px;
                font-weight: 600;
                color: #172033;
            }

            QLabel[role="error"] {
                color: #dc2626;
                font-size: 12px;
            }
        """)

        # -----------------------------------------------------
        # Main page layout
        # -----------------------------------------------------

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        # -----------------------------------------------------
        # Page heading
        # -----------------------------------------------------

        title = QLabel("Battery Diagnostics")
        title.setProperty(
            "role",
            "title",
        )

        subtitle = QLabel(
            "Enter battery information to perform a complete "
            "health assessment."
        )

        subtitle.setProperty(
            "role",
            "subtitle",
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # -----------------------------------------------------
        # Battery information card
        # -----------------------------------------------------

        input_card = QFrame()
        input_card.setProperty(
            "role",
            "card",
        )

        input_layout = QVBoxLayout(
            input_card
        )

        input_layout.setContentsMargins(
            12,
            10,
            12,
            10,
        )

        input_layout.setSpacing(8)

        section_title = QLabel(
            "Battery Information"
        )

        section_title.setProperty(
            "role",
            "section",
        )

        input_layout.addWidget(
            section_title
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        form = QFormLayout()

        form.setSpacing(10)

        form.setHorizontalSpacing(16)

        form.setFieldGrowthPolicy(
            QFormLayout.AllNonFixedFieldsGrow
        )

        # -----------------------------------------------------
        # Chemistry
        # -----------------------------------------------------

        self.chemistry = QComboBox()

        self.chemistry.addItems([
            "Lithium-ion (NMC)",
            "Lithium-ion (LFP)",
            "Lithium-ion (NCA)",
            "Lithium-ion (LCO)",
            "Lead-acid",
            "Other",
        ])

        self.chemistry.setMinimumWidth(300)

        form.addRow(
            "Battery Chemistry:",
            self.chemistry,
        )

        # -----------------------------------------------------
        # Rated capacity
        # -----------------------------------------------------

        self.rated_capacity = QLineEdit()

        self.rated_capacity.setPlaceholderText(
            "e.g. 60"
        )

        self.rated_capacity.setMinimumWidth(300)

        form.addRow(
            "Rated Capacity (kWh):",
            self.rated_capacity,
        )

        # -----------------------------------------------------
        # Current capacity
        # -----------------------------------------------------

        self.current_capacity = QLineEdit()

        self.current_capacity.setPlaceholderText(
            "e.g. 52"
        )

        self.current_capacity.setMinimumWidth(300)

        form.addRow(
            "Current Capacity (kWh):",
            self.current_capacity,
        )

        # -----------------------------------------------------
        # Battery age
        # -----------------------------------------------------

        self.battery_age = QLineEdit()

        self.battery_age.setPlaceholderText(
            "e.g. 4"
        )

        self.battery_age.setMinimumWidth(300)

        form.addRow(
            "Battery Age (years):",
            self.battery_age,
        )

        # -----------------------------------------------------
        # Original battery value
        # -----------------------------------------------------

        self.original_value = QLineEdit()

        self.original_value.setPlaceholderText(
            "e.g. 1000000"
        )

        self.original_value.setMinimumWidth(300)

        form.addRow(
            "Original Battery Value (INR):",
            self.original_value,
        )

        # -----------------------------------------------------
        # Pack voltage
        # -----------------------------------------------------

        self.pack_voltage = QLineEdit()

        self.pack_voltage.setPlaceholderText(
            "e.g. 400"
        )

        self.pack_voltage.setMinimumWidth(300)

        form.addRow(
            "Pack Voltage (V):",
            self.pack_voltage,
        )

        # -----------------------------------------------------
        # Current
        # -----------------------------------------------------

        self.current = QLineEdit()

        self.current.setPlaceholderText(
            "e.g. 120"
        )

        self.current.setMinimumWidth(300)

        form.addRow(
            "Current (A):",
            self.current,
        )

        # -----------------------------------------------------
        # Temperature
        # -----------------------------------------------------

        self.temperature = QLineEdit()

        self.temperature.setPlaceholderText(
            "e.g. 28"
        )

        self.temperature.setMinimumWidth(300)

        form.addRow(
            "Temperature (°C):",
            self.temperature,
        )

        # -----------------------------------------------------
        # Cycle count
        # -----------------------------------------------------

        self.cycle_count = QLineEdit()

        self.cycle_count.setPlaceholderText(
            "e.g. 842"
        )

        self.cycle_count.setMinimumWidth(300)

        form.addRow(
            "Cycle Count:",
            self.cycle_count,
        )

        # -----------------------------------------------------
        # Annual degradation
        # -----------------------------------------------------

        self.annual_degradation = QLineEdit()

        self.annual_degradation.setPlaceholderText(
            "e.g. 2.8"
        )

        self.annual_degradation.setMinimumWidth(300)

        form.addRow(
            "Annual Degradation (%/year):",
            self.annual_degradation,
        )

        input_layout.addLayout(form)

        # -----------------------------------------------------
        # Hint
        # -----------------------------------------------------

        hint = QLabel(
            "Annual degradation is used by the prototype RUL "
            "model. It should come from historical battery "
            "data when available."
        )

        hint.setProperty(
            "role",
            "hint",
        )

        input_layout.addWidget(hint)

        layout.addWidget(
            input_card
        )

        # -----------------------------------------------------
        # Results card
        # -----------------------------------------------------

        result_card = QFrame()

        result_card.setProperty(
            "role",
            "card",
        )

        result_layout = QHBoxLayout(
            result_card
        )

        result_layout.setContentsMargins(
            12,
            10,
            12,
            10,
        )

        result_layout.setSpacing(8)

        # -----------------------------------------------------
        # SoH result
        # -----------------------------------------------------

        soh_container = QVBoxLayout()

        soh_label = QLabel(
            "STATE OF HEALTH"
        )

        soh_label.setProperty(
            "role",
            "result_label",
        )

        self.soh_value = QLabel("--")

        self.soh_value.setProperty(
            "role",
            "result_value",
        )

        soh_container.addWidget(
            soh_label
        )

        soh_container.addWidget(
            self.soh_value
        )

        # -----------------------------------------------------
        # Capacity degradation
        # -----------------------------------------------------

        degradation_container = QVBoxLayout()

        degradation_label = QLabel(
            "CAPACITY LOSS"
        )

        degradation_label.setProperty(
            "role",
            "result_label",
        )

        self.degradation_value = QLabel(
            "--"
        )

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

        # -----------------------------------------------------
        # Health status
        # -----------------------------------------------------

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
            "status",
        )

        status_container.addWidget(
            status_label
        )

        status_container.addWidget(
            self.status_value
        )

        # -----------------------------------------------------
        # RUL
        # -----------------------------------------------------

        rul_container = QVBoxLayout()

        rul_label = QLabel(
            "ESTIMATED RUL"
        )

        rul_label.setProperty(
            "role",
            "result_label",
        )

        self.rul_value = QLabel(
            "--"
        )

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

        # -----------------------------------------------------
        # Add result sections
        # -----------------------------------------------------

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

        layout.addWidget(
            result_card
        )

        # -----------------------------------------------------
        # RUL status message
        # -----------------------------------------------------

        self.rul_status = QLabel("")

        self.rul_status.setProperty(
            "role",
            "hint",
        )

        layout.addWidget(
            self.rul_status
        )

        # -----------------------------------------------------
        # Error message
        # -----------------------------------------------------

        self.error_label = QLabel("")

        self.error_label.setProperty(
            "role",
            "error",
        )

        layout.addWidget(
            self.error_label
        )

        # -----------------------------------------------------
        # Action button
        # -----------------------------------------------------

        action_row = QHBoxLayout()

        action_row.addStretch()

        assessment_button = QPushButton(
            "Run Battery Assessment"
        )

        assessment_button.setObjectName(
            "assessment_button"
        )

        assessment_button.clicked.connect(
            self.run_assessment
        )

        action_row.addWidget(
            assessment_button
        )

        layout.addLayout(
            action_row
        )

        layout.addStretch()

    # =========================================================
    # BATTERY ASSESSMENT
    # =========================================================

    def run_assessment(self):
        """
        Read the form and calculate:

        1. State of Health
        2. Total capacity loss
        3. Health classification
        4. Estimated RUL

        The completed result is also emitted through
        analysis_completed so MainWindow can pass it to
        ReportsView.
        """

        self.error_label.setText("")
        self.rul_status.setText("")

        try:

            # -------------------------------------------------
            # Read required values
            # -------------------------------------------------

            rated_capacity = float(
                self.rated_capacity.text()
            )

            current_capacity = float(
                self.current_capacity.text()
            )

            annual_degradation = float(
                self.annual_degradation.text()
            )

            # -------------------------------------------------
            # Basic validation
            # -------------------------------------------------

            if rated_capacity <= 0:
                raise ValueError(
                    "Rated capacity must be greater than 0."
                )

            if current_capacity < 0:
                raise ValueError(
                    "Current capacity cannot be negative."
                )

            if current_capacity > rated_capacity:
                raise ValueError(
                    "Current capacity cannot exceed rated capacity."
                )

            if annual_degradation <= 0:
                raise ValueError(
                    "Annual degradation must be greater than 0."
                )

            # -------------------------------------------------
            # Battery health calculations
            # -------------------------------------------------

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

            # -------------------------------------------------
            # RUL calculation
            # -------------------------------------------------

            rul_years = estimate_rul_years(
                current_soh=soh,
                annual_degradation_rate=(
                    annual_degradation
                ),
            )

            rul_classification = classify_rul(
                rul_years
            )

            # -------------------------------------------------
            # Display results
            # -------------------------------------------------

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
                f"RUL assessment: "
                f"{rul_classification}"
            )

            # -------------------------------------------------
            # Store analysis result
            # -------------------------------------------------

            self.analysis_result = {
                "health": {
                    "soh": round(
                        soh,
                        2,
                    ),
                    "classification": (
                        health_status
                    ),
                    "capacity_degradation": round(
                        capacity_loss,
                        2,
                    ),
                },

                "rul": {
                    "years": round(
                        rul_years,
                        2,
                    ),
                    "classification": (
                        rul_classification
                    ),
                },
            }

            # -------------------------------------------------
            # Notify MainWindow
            # -------------------------------------------------

            self.analysis_completed.emit(
                self.analysis_result
            )

        except ValueError as error:

            # -------------------------------------------------
            # Reset visible results
            # -------------------------------------------------

            self.soh_value.setText(
                "--"
            )

            self.degradation_value.setText(
                "--"
            )

            self.status_value.setText(
                "Assessment failed"
            )

            self.rul_value.setText(
                "--"
            )

            self.rul_status.setText(
                ""
            )

            self.analysis_result = None

            self.error_label.setText(
                f"Please enter valid values. "
                f"{error}"
            )