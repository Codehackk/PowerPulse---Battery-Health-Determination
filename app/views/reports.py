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

            QTextEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
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

            QLabel[role="hint"] {
                color: #64748b;
                font-size: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # ---------------------------------------------------------
        # Page heading
        # ---------------------------------------------------------

        title = QLabel("Battery Reports")
        title.setProperty("role", "title")

        subtitle = QLabel(
            "Generate a consolidated summary of battery "
            "health, RUL, valuation, and second-life results."
        )
        subtitle.setProperty("role", "subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------------------------------------------------------
        # Report overview card
        # ---------------------------------------------------------

        overview_card = QFrame()
        overview_card.setProperty("role", "card")

        overview_layout = QVBoxLayout(
            overview_card
        )

        section_title = QLabel("Report Overview")
        section_title.setProperty(
            "role",
            "section",
        )

        overview_layout.addWidget(
            section_title
        )

        metrics_row = QHBoxLayout()

        # SoH
        soh_container = QVBoxLayout()

        soh_label = QLabel("STATE OF HEALTH")
        soh_label.setProperty(
            "role",
            "result_label",
        )

        self.soh_result = QLabel("--")
        self.soh_result.setProperty(
            "role",
            "result_value",
        )

        soh_container.addWidget(soh_label)
        soh_container.addWidget(
            self.soh_result
        )

        # RUL
        rul_container = QVBoxLayout()

        rul_label = QLabel("RUL")
        rul_label.setProperty(
            "role",
            "result_label",
        )

        self.rul_result = QLabel("--")
        self.rul_result.setProperty(
            "role",
            "result_value",
        )

        rul_container.addWidget(rul_label)
        rul_container.addWidget(
            self.rul_result
        )

        # Valuation
        valuation_container = QVBoxLayout()

        valuation_label = QLabel(
            "RESIDUAL VALUE"
        )
        valuation_label.setProperty(
            "role",
            "result_label",
        )

        self.valuation_result = QLabel("--")
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

        # Second life
        second_life_container = QVBoxLayout()

        second_life_label = QLabel(
            "SECOND-LIFE SCORE"
        )
        second_life_label.setProperty(
            "role",
            "result_label",
        )

        self.second_life_result = QLabel("--")
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

        metrics_row.addLayout(soh_container)
        metrics_row.addLayout(rul_container)
        metrics_row.addLayout(
            valuation_container
        )
        metrics_row.addLayout(
            second_life_container
        )

        overview_layout.addLayout(
            metrics_row
        )

        layout.addWidget(overview_card)

        # ---------------------------------------------------------
        # Report text card
        # ---------------------------------------------------------

        report_card = QFrame()
        report_card.setProperty("role", "card")

        report_layout = QVBoxLayout(
            report_card
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

        self.report_text.setReadOnly(True)

        self.report_text.setPlaceholderText(
            "Your battery assessment report will appear here."
        )

        report_layout.addWidget(
            self.report_text
        )

        layout.addWidget(report_card)

        # ---------------------------------------------------------
        # Action
        # ---------------------------------------------------------

        action_row = QHBoxLayout()

        hint = QLabel(
            "Prototype report data is currently "
            "generated from demonstration values."
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

        action_row.addWidget(hint)
        action_row.addStretch()
        action_row.addWidget(
            generate_button
        )

        layout.addLayout(action_row)

        layout.addStretch()

    def generate_report(self):
        """Generate a demonstration battery report."""

        report = generate_battery_report(
            soh=86.7,
            health_class="Healthy",
            rul_years=6.0,
            residual_value=760200.0,
            value_retention=76.02,
            second_life_score=76.02,
            second_life_suitability="Highly Suitable",
            recommended_application=(
                "Stationary Energy Storage"
            ),
        )

        self.soh_result.setText(
            f"{report['battery_health']['soh']:.2f}%"
        )

        self.rul_result.setText(
            f"{report['remaining_useful_life']['years']:.2f} years"
        )

        self.valuation_result.setText(
            f"{report['valuation']['residual_value']:.2f}"
        )

        self.second_life_result.setText(
            f"{report['second_life']['score']:.2f}/100"
        )

        self.report_text.setPlainText(
            create_report_summary(report)
        )