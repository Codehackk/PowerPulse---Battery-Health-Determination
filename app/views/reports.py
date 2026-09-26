from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QTextEdit,
)

from app.core.reports import (
    generate_battery_report,
    create_report_summary,
)


class ReportsView(QWidget):

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

            QLabel[role="result_label"] {
                font-size: 11px;
                font-weight: 600;
                color: #64748b;
            }

            QLabel[role="result_value"] {
                font-size: 20px;
                font-weight: 700;
                color: #172033;
            }

            QLabel[role="status"] {
                font-size: 14px;
                font-weight: 600;
                color: #172033;
            }

            QTextEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                color: #172033;
            }

            QPushButton#generate_button {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 11px 20px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#generate_button:hover {
                background-color: #1d4ed8;
            }

            QPushButton#generate_button:pressed {
                background-color: #1e40af;
            }

            QLabel[role="hint"] {
                color: #64748b;
                font-size: 12px;
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

        title = QLabel(
            "Battery Reports"
        )

        title.setProperty(
            "role",
            "title",
        )

        subtitle = QLabel(
            "Generate a consolidated summary of battery "
            "health, RUL, valuation, and second-life results."
        )

        subtitle.setProperty(
            "role",
            "subtitle",
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # -----------------------------------------------------
        # Report overview card
        # -----------------------------------------------------

        overview_card = QFrame()

        overview_card.setProperty(
            "role",
            "card",
        )

        overview_layout = QVBoxLayout(
            overview_card
        )

        overview_layout.setContentsMargins(
            12,
            10,
            12,
            10,
        )

        section_title = QLabel(
            "Report Overview"
        )

        section_title.setProperty(
            "role",
            "section",
        )

        overview_layout.addWidget(
            section_title
        )

        # -----------------------------------------------------
        # Metrics row
        # -----------------------------------------------------

        metrics_row = QHBoxLayout()

        metrics_row.setSpacing(16)

        # -----------------------------------------------------
        # SoH
        # -----------------------------------------------------

        soh_container = QVBoxLayout()

        soh_label = QLabel(
            "STATE OF HEALTH"
        )

        soh_label.setProperty(
            "role",
            "result_label",
        )

        self.soh_result = QLabel(
            "--"
        )

        self.soh_result.setProperty(
            "role",
            "result_value",
        )

        soh_container.addWidget(
            soh_label
        )

        soh_container.addWidget(
            self.soh_result
        )

        # -----------------------------------------------------
        # RUL
        # -----------------------------------------------------

        rul_container = QVBoxLayout()

        rul_label = QLabel(
            "RUL"
        )

        rul_label.setProperty(
            "role",
            "result_label",
        )

        self.rul_result = QLabel(
            "--"
        )

        self.rul_result.setProperty(
            "role",
            "result_value",
        )

        rul_container.addWidget(
            rul_label
        )

        rul_container.addWidget(
            self.rul_result
        )

        # -----------------------------------------------------
        # Valuation
        # -----------------------------------------------------

        valuation_container = QVBoxLayout()

        valuation_label = QLabel(
            "RESIDUAL VALUE"
        )

        valuation_label.setProperty(
            "role",
            "result_label",
        )

        self.valuation_result = QLabel(
            "--"
        )

        self.valuation_result.setProperty(
            "role",
            "result_value",
        )

        valuation_container.addWidget(
            valuation_label
        )

        valuation_container.addWidget(
            self.valuation_result
        )

        # -----------------------------------------------------
        # Second life
        # -----------------------------------------------------

        second_life_container = QVBoxLayout()

        second_life_label = QLabel(
            "SECOND-LIFE SCORE"
        )

        second_life_label.setProperty(
            "role",
            "result_label",
        )

        self.second_life_result = QLabel(
            "--"
        )

        self.second_life_result.setProperty(
            "role",
            "result_value",
        )

        second_life_container.addWidget(
            second_life_label
        )

        second_life_container.addWidget(
            self.second_life_result
        )

        # -----------------------------------------------------
        # Add metrics
        # -----------------------------------------------------

        metrics_row.addLayout(
            soh_container
        )

        metrics_row.addLayout(
            rul_container
        )

        metrics_row.addLayout(
            valuation_container
        )

        metrics_row.addLayout(
            second_life_container
        )

        overview_layout.addLayout(
            metrics_row
        )

        layout.addWidget(
            overview_card
        )

        # -----------------------------------------------------
        # Generated report card
        # -----------------------------------------------------

        report_card = QFrame()

        report_card.setProperty(
            "role",
            "card",
        )

        report_layout = QVBoxLayout(
            report_card
        )

        report_layout.setContentsMargins(
            12,
            10,
            12,
            10,
        )

        report_title = QLabel(
            "Generated Report"
        )

        report_title.setProperty(
            "role",
            "section",
        )

        report_layout.addWidget(
            report_title
        )

        self.report_text = QTextEdit()

        self.report_text.setReadOnly(
            True
        )

        self.report_text.setPlaceholderText(
            "Your battery assessment report "
            "will appear here after an assessment."
        )

        report_layout.addWidget(
            self.report_text
        )

        layout.addWidget(
            report_card
        )

        # -----------------------------------------------------
        # Error message
        # -----------------------------------------------------

        self.error_label = QLabel(
            ""
        )

        self.error_label.setProperty(
            "role",
            "error",
        )

        layout.addWidget(
            self.error_label
        )

        # -----------------------------------------------------
        # Action row
        # -----------------------------------------------------

        action_row = QHBoxLayout()

        hint = QLabel(
            "Run a battery assessment from Diagnostics "
            "to populate the report."
        )

        hint.setProperty(
            "role",
            "hint",
        )

        generate_button = QPushButton(
            "Generate Report"
        )

        generate_button.setObjectName(
            "generate_button"
        )

        generate_button.clicked.connect(
            self.generate_report
        )

        action_row.addWidget(
            hint
        )

        action_row.addStretch()

        action_row.addWidget(
            generate_button
        )

        layout.addLayout(
            action_row
        )

        layout.addStretch()

    # =========================================================
    # RECEIVE DIAGNOSTICS RESULT
    # =========================================================

    def update_from_analysis(
        self,
        analysis,
    ):
        """
        Receive the completed Diagnostics result.

        This method is connected to:

            DiagnosticsView.analysis_completed

        by MainWindow.
        """

        self.error_label.setText(
            ""
        )

        self.analysis_result = analysis

        if not analysis:
            return

        # -----------------------------------------------------
        # Extract health information
        # -----------------------------------------------------

        health = analysis.get(
            "health",
            {},
        )

        # -----------------------------------------------------
        # Extract RUL information
        # -----------------------------------------------------

        rul = analysis.get(
            "rul",
            {},
        )

        # -----------------------------------------------------
        # Extract valuation information
        # -----------------------------------------------------

        valuation = analysis.get(
            "valuation",
            {},
        )

        # -----------------------------------------------------
        # Extract second-life information
        # -----------------------------------------------------

        second_life = analysis.get(
            "second_life",
            {},
        )

        # -----------------------------------------------------
        # SoH
        # -----------------------------------------------------

        soh = health.get(
            "soh"
        )

        if soh is not None:

            self.soh_result.setText(
                f"{soh:.2f}%"
            )

        else:

            self.soh_result.setText(
                "--"
            )

        # -----------------------------------------------------
        # RUL
        # -----------------------------------------------------

        rul_years = rul.get(
            "years"
        )

        if rul_years is not None:

            self.rul_result.setText(
                f"{rul_years:.2f} years"
            )

        else:

            self.rul_result.setText(
                "--"
            )

        # -----------------------------------------------------
        # Valuation
        # -----------------------------------------------------

        residual_value = valuation.get(
            "residual_value"
        )

        if residual_value is not None:

            self.valuation_result.setText(
                f"₹{residual_value:,.2f}"
            )

        else:

            self.valuation_result.setText(
                "--"
            )

        # -----------------------------------------------------
        # Second-life
        # -----------------------------------------------------

        second_life_score = second_life.get(
            "score"
        )

        if second_life_score is not None:

            self.second_life_result.setText(
                f"{second_life_score:.2f}/100"
            )

        else:

            self.second_life_result.setText(
                "--"
            )

        # -----------------------------------------------------
        # Build report text
        # -----------------------------------------------------

        health_class = health.get(
            "classification",
            "Unknown",
        )

        capacity_degradation = health.get(
            "capacity_degradation"
        )

        rul_class = rul.get(
            "classification",
            "Unknown",
        )

        value_retention = valuation.get(
            "value_retention"
        )

        value_class = valuation.get(
            "classification",
            "Unknown",
        )

        second_life_suitability = (
            second_life.get(
                "suitability",
                "Unknown",
            )
        )

        recommended_application = (
            second_life.get(
                "recommended_application",
                "Unknown",
            )
        )

        report_lines = [
            "BATTERY ASSESSMENT REPORT",
            "",
            "----------------------------------------",
            "BATTERY HEALTH",
            "----------------------------------------",
            (
                f"SoH: {soh:.2f}%"
                if soh is not None
                else "SoH: --"
            ),
            f"Health Classification: {health_class}",
            (
                f"Capacity Loss: "
                f"{capacity_degradation:.2f}%"
                if capacity_degradation is not None
                else "Capacity Loss: --"
            ),
            "",
            "----------------------------------------",
            "REMAINING USEFUL LIFE",
            "----------------------------------------",
            (
                f"Estimated RUL: "
                f"{rul_years:.2f} years"
                if rul_years is not None
                else "Estimated RUL: --"
            ),
            f"RUL Classification: {rul_class}",
            "",
            "----------------------------------------",
            "VALUATION",
            "----------------------------------------",
            (
                f"Residual Value: "
                f"₹{residual_value:,.2f}"
                if residual_value is not None
                else "Residual Value: --"
            ),
            (
                f"Value Retention: "
                f"{value_retention:.2f}%"
                if value_retention is not None
                else "Value Retention: --"
            ),
            f"Valuation Classification: {value_class}",
            "",
            "----------------------------------------",
            "SECOND-LIFE ASSESSMENT",
            "----------------------------------------",
            (
                f"Suitability Score: "
                f"{second_life_score:.2f}/100"
                if second_life_score is not None
                else "Suitability Score: --"
            ),
            (
                f"Suitability: "
                f"{second_life_suitability}"
            ),
            (
                f"Recommended Application: "
                f"{recommended_application}"
            ),
        ]

        self.report_text.setPlainText(
            "\n".join(report_lines)
        )

    # =========================================================
    # GENERATE REPORT
    # =========================================================

    def generate_report(self):
        """
        Generate the report from the latest analysis.

        If Diagnostics has already supplied a complete
        analysis, use that data.

        Otherwise, show a message instead of silently
        using demonstration values.
        """

        self.error_label.setText(
            ""
        )

        # -----------------------------------------------------
        # Require an actual assessment
        # -----------------------------------------------------

        if not self.analysis_result:

            self.error_label.setText(
                "No battery assessment is available. "
                "Run an assessment from Diagnostics first."
            )

            return

        try:

            analysis = self.analysis_result

            health = analysis.get(
                "health",
                {},
            )

            rul = analysis.get(
                "rul",
                {},
            )

            valuation = analysis.get(
                "valuation",
                {},
            )

            second_life = analysis.get(
                "second_life",
                {},
            )

            # -------------------------------------------------
            # Read values
            # -------------------------------------------------

            soh = health.get(
                "soh",
                0.0,
            )

            health_class = health.get(
                "classification",
                "Unknown",
            )

            rul_years = rul.get(
                "years",
                0.0,
            )

            residual_value = valuation.get(
                "residual_value",
                0.0,
            )

            value_retention = valuation.get(
                "value_retention",
                0.0,
            )

            second_life_score = second_life.get(
                "score",
                0.0,
            )

            second_life_suitability = (
                second_life.get(
                    "suitability",
                    "Unknown",
                )
            )

            recommended_application = (
                second_life.get(
                    "recommended_application",
                    "Unknown",
                )
            )

            # -------------------------------------------------
            # Generate structured report
            # -------------------------------------------------

            report = generate_battery_report(
                soh=soh,
                health_class=health_class,
                rul_years=rul_years,
                residual_value=residual_value,
                value_retention=value_retention,
                second_life_score=second_life_score,
                second_life_suitability=(
                    second_life_suitability
                ),
                recommended_application=(
                    recommended_application
                ),
            )

            # -------------------------------------------------
            # Update overview
            # -------------------------------------------------

            self.soh_result.setText(
                f"{report['battery_health']['soh']:.2f}%"
            )

            self.rul_result.setText(
                f"{report['remaining_useful_life']['years']:.2f} years"
            )

            self.valuation_result.setText(
                f"₹{report['valuation']['residual_value']:,.2f}"
            )

            self.second_life_result.setText(
                f"{report['second_life']['score']:.2f}/100"
            )

            # -------------------------------------------------
            # Generate summary
            # -------------------------------------------------

            self.report_text.setPlainText(
                create_report_summary(
                    report
                )
            )

        except Exception as error:

            self.error_label.setText(
                f"Unable to generate report. {error}"
            )