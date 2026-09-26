from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QFormLayout,
)

from app.core.settings import (
    get_application_settings,
)


class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = get_application_settings()

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

            QLabel[role="label"] {
                color: #64748b;
                font-size: 13px;
            }

            QLabel[role="value"] {
                color: #172033;
                font-size: 13px;
                font-weight: 600;
            }

            QLabel[role="prototype"] {
                color: #2563eb;
                font-size: 13px;
                font-weight: 700;
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

        title = QLabel("Settings")
        title.setProperty("role", "title")

        subtitle = QLabel(
            "View PowerPulse application configuration "
            "and model assumptions."
        )
        subtitle.setProperty("role", "subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------------------------------------------------------
        # Application information
        # ---------------------------------------------------------

        app_card = QFrame()
        app_card.setProperty("role", "card")

        app_layout = QVBoxLayout(app_card)

        app_title = QLabel("Application")
        app_title.setProperty("role", "section")

        app_layout.addWidget(app_title)

        app_form = QFormLayout()
        app_form.setSpacing(12)

        version_label = QLabel("Application Version")
        version_label.setProperty("role", "label")

        version_value = QLabel(
            self.settings["app_version"]
        )
        version_value.setProperty("role", "value")

        environment_label = QLabel("Environment")
        environment_label.setProperty(
            "role",
            "label",
        )

        environment_value = QLabel(
            self.settings["environment"]
        )
        environment_value.setProperty(
            "role",
            "prototype",
        )

        currency_label = QLabel("Default Currency")
        currency_label.setProperty(
            "role",
            "label",
        )

        currency_value = QLabel(
            self.settings["currency"]
        )
        currency_value.setProperty(
            "role",
            "value",
        )

        app_form.addRow(
            version_label,
            version_value,
        )

        app_form.addRow(
            environment_label,
            environment_value,
        )

        app_form.addRow(
            currency_label,
            currency_value,
        )

        app_layout.addLayout(app_form)

        layout.addWidget(app_card)

        # ---------------------------------------------------------
        # Battery model settings
        # ---------------------------------------------------------

        model_card = QFrame()
        model_card.setProperty("role", "card")

        model_layout = QVBoxLayout(model_card)

        model_title = QLabel(
            "Battery Model Settings"
        )
        model_title.setProperty(
            "role",
            "section",
        )

        model_layout.addWidget(model_title)

        model_form = QFormLayout()
        model_form.setSpacing(12)

        reference_label = QLabel(
            "Second-Life Reference Period"
        )
        reference_label.setProperty(
            "role",
            "label",
        )

        reference_value = QLabel(
            f"{self.settings['second_life_reference_years']:.1f} years"
        )
        reference_value.setProperty(
            "role",
            "value",
        )

        model_form.addRow(
            reference_label,
            reference_value,
        )

        model_layout.addLayout(model_form)

        layout.addWidget(model_card)

        # ---------------------------------------------------------
        # SoH thresholds
        # ---------------------------------------------------------

        threshold_card = QFrame()
        threshold_card.setProperty(
            "role",
            "card",
        )

        threshold_layout = QVBoxLayout(
            threshold_card
        )

        threshold_title = QLabel(
            "State of Health Thresholds"
        )
        threshold_title.setProperty(
            "role",
            "section",
        )

        threshold_layout.addWidget(
            threshold_title
        )

        threshold_row = QHBoxLayout()

        thresholds = self.settings[
            "soh_thresholds"
        ]

        healthy_container = QVBoxLayout()

        healthy_label = QLabel("Healthy")
        healthy_label.setProperty(
            "role",
            "label",
        )

        healthy_value = QLabel(
            f">= {thresholds['healthy']:.0f}%"
        )
        healthy_value.setProperty(
            "role",
            "value",
        )

        healthy_container.addWidget(
            healthy_label
        )
        healthy_container.addWidget(
            healthy_value
        )

        moderate_container = QVBoxLayout()

        moderate_label = QLabel("Moderate")
        moderate_label.setProperty(
            "role",
            "label",
        )

        moderate_value = QLabel(
            f">= {thresholds['moderate']:.0f}%"
        )
        moderate_value.setProperty(
            "role",
            "value",
        )

        moderate_container.addWidget(
            moderate_label
        )
        moderate_container.addWidget(
            moderate_value
        )

        degraded_container = QVBoxLayout()

        degraded_label = QLabel("Degraded")
        degraded_label.setProperty(
            "role",
            "label",
        )

        degraded_value = QLabel(
            f">= {thresholds['degraded']:.0f}%"
        )
        degraded_value.setProperty(
            "role",
            "value",
        )

        degraded_container.addWidget(
            degraded_label
        )
        degraded_container.addWidget(
            degraded_value
        )

        threshold_row.addLayout(
            healthy_container
        )

        threshold_row.addLayout(
            moderate_container
        )

        threshold_row.addLayout(
            degraded_container
        )

        threshold_layout.addLayout(
            threshold_row
        )

        layout.addWidget(threshold_card)

        # ---------------------------------------------------------
        # Information
        # ---------------------------------------------------------

        info_card = QFrame()
        info_card.setProperty(
            "role",
            "card",
        )

        info_layout = QVBoxLayout(info_card)

        info_title = QLabel(
            "Prototype Configuration"
        )
        info_title.setProperty(
            "role",
            "section",
        )

        info_layout.addWidget(
            info_title
        )

        info_text = QLabel(
            "PowerPulse is currently running in "
            "prototype mode. Model thresholds and "
            "assumptions can be refined as verified "
            "research data becomes available."
        )

        info_text.setWordWrap(True)
        info_text.setProperty(
            "role",
            "hint",
        )

        info_layout.addWidget(
            info_text
        )

        layout.addWidget(info_card)

        layout.addStretch()