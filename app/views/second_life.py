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

from app.core.second_life import (
    calculate_second_life_score,
    classify_second_life_suitability,
    recommend_second_life_application,
)


class SecondLifeView(QWidget):
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

            QPushButton#assess_button {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 11px 20px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#assess_button:hover {
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
                font-size: 22px;
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

        title = QLabel("Second-Life Assessment")
        title.setProperty("role", "title")

        subtitle = QLabel(
            "Assess whether a battery may be suitable for "
            "potential second-life applications."
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

        section_title = QLabel("Battery Parameters")
        section_title.setProperty("role", "section")

        input_layout.addWidget(section_title)

        form = QFormLayout()
        form.setSpacing(12)

        self.soh_input = QLineEdit()
        self.soh_input.setPlaceholderText("e.g. 86.7")

        self.rul_input = QLineEdit()
        self.rul_input.setPlaceholderText("e.g. 6.0")

        form.addRow(
            "Current State of Health (%):",
            self.soh_input,
        )

        form.addRow(
            "Remaining Useful Life (years):",
            self.rul_input,
        )

        input_layout.addLayout(form)

        hint = QLabel(
            "The current prototype uses SoH and RUL to "
            "estimate second-life suitability."
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

        # Score
        score_container = QVBoxLayout()

        score_label = QLabel("SUITABILITY SCORE")
        score_label.setProperty(
            "role",
            "result_label",
        )

        self.score_result = QLabel("--")
        self.score_result.setProperty(
            "role",
            "result_value",
        )

        score_container.addWidget(score_label)
        score_container.addWidget(self.score_result)

        # Suitability
        suitability_container = QVBoxLayout()

        suitability_label = QLabel("SUITABILITY")
        suitability_label.setProperty(
            "role",
            "result_label",
        )

        self.suitability_result = QLabel(
            "Awaiting assessment"
        )
        self.suitability_result.setProperty(
            "role",
            "status",
        )

        suitability_container.addWidget(
            suitability_label
        )
        suitability_container.addWidget(
            self.suitability_result
        )

        # Application
        application_container = QVBoxLayout()

        application_label = QLabel(
            "RECOMMENDED APPLICATION"
        )
        application_label.setProperty(
            "role",
            "result_label",
        )

        self.application_result = QLabel("--")
        self.application_result.setProperty(
            "role",
            "result_value",
        )

        application_container.addWidget(
            application_label
        )
        application_container.addWidget(
            self.application_result
        )

        result_layout.addLayout(score_container)
        result_layout.addLayout(
            suitability_container
        )
        result_layout.addLayout(
            application_container
        )

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
        # Assess button
        # ---------------------------------------------------------

        action_row = QHBoxLayout()

        assess_button = QPushButton(
            "Assess Second-Life Suitability"
        )

        assess_button.setObjectName(
            "assess_button"
        )

        assess_button.clicked.connect(
            self.assess_second_life
        )

        action_row.addStretch()
        action_row.addWidget(
            assess_button
        )

        layout.addLayout(action_row)

        layout.addStretch()

    def assess_second_life(self):
        """Assess second-life suitability."""

        self.error_label.setText("")

        try:
            current_soh = float(
                self.soh_input.text()
            )

            current_rul_years = float(
                self.rul_input.text()
            )

            score = calculate_second_life_score(
                soh=current_soh,
                rul_years=current_rul_years,
            )

            suitability = (
                classify_second_life_suitability(
                    score
                )
            )

            application = (
                recommend_second_life_application(
                    score=score,
                    soh=current_soh,
                )
            )

            self.score_result.setText(
                f"{score:.2f}/100"
            )

            self.suitability_result.setText(
                suitability
            )

            self.application_result.setText(
                application
            )

        except ValueError as error:

            self.score_result.setText("--")

            self.suitability_result.setText(
                "Assessment failed"
            )

            self.application_result.setText("--")

            self.error_label.setText(
                f"Please enter valid values. {error}"
            )