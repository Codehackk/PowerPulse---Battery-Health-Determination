from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        # Dashboard styling
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f7fb;
                color: #172033;
                font-family: "Segoe UI";
            }

            QFrame {
                background-color: white;
                border: 1px solid #dfe5ee;
                border-radius: 12px;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel[role="title"] {
                font-size: 28px;
                font-weight: 700;
                color: #172033;
            }

            QLabel[role="subtitle"] {
                font-size: 14px;
                color: #64748b;
                padding-bottom: 12px;
            }

            QLabel[role="metric_label"] {
                font-size: 11px;
                font-weight: 600;
                color: #64748b;
            }

            QLabel[role="metric"] {
                font-size: 32px;
                font-weight: 700;
                color: #172033;
                padding: 8px 0;
            }

            QLabel[role="status"] {
                font-size: 12px;
                color: #64748b;
            }
        """)

        layout = QVBoxLayout(self)

        # Dashboard heading
        title = QLabel("Battery Overview")
        title.setProperty("role", "title")

        subtitle = QLabel(
            "Monitor battery health, degradation, and lifecycle status."
        )
        subtitle.setProperty("role", "subtitle")

        # ---------------------------------------------------------
        # Battery Health Card
        # ---------------------------------------------------------

        health_card = QFrame()
        health_card_layout = QVBoxLayout(health_card)

        health_label = QLabel("AVERAGE BATTERY HEALTH")
        health_label.setProperty("role", "metric_label")

        health_value = QLabel("87%")
        health_value.setProperty("role", "metric")

        health_status = QLabel("Healthy")
        health_status.setProperty("role", "status")

        health_card_layout.addWidget(health_label)
        health_card_layout.addWidget(health_value)
        health_card_layout.addWidget(health_status)

        # ---------------------------------------------------------
        # Remaining Useful Life Card
        # ---------------------------------------------------------

        rul_card = QFrame()
        rul_card_layout = QVBoxLayout(rul_card)

        rul_label = QLabel("ESTIMATED REMAINING LIFE")
        rul_label.setProperty("role", "metric_label")

        rul_value = QLabel("4.8 Years")
        rul_value.setProperty("role", "metric")

        rul_status = QLabel("Within expected lifecycle")
        rul_status.setProperty("role", "status")

        rul_card_layout.addWidget(rul_label)
        rul_card_layout.addWidget(rul_value)
        rul_card_layout.addWidget(rul_status)

        # ---------------------------------------------------------
        # Cycle Count Card
        # ---------------------------------------------------------

        cycle_card = QFrame()
        cycle_card_layout = QVBoxLayout(cycle_card)

        cycle_label = QLabel("CYCLE COUNT")
        cycle_label.setProperty("role", "metric_label")

        cycle_value = QLabel("842")
        cycle_value.setProperty("role", "metric")

        cycle_status = QLabel("Moderate usage")
        cycle_status.setProperty("role", "status")

        cycle_card_layout.addWidget(cycle_label)
        cycle_card_layout.addWidget(cycle_value)
        cycle_card_layout.addWidget(cycle_status)

        # ---------------------------------------------------------
        # Degradation Rate Card
        # ---------------------------------------------------------

        degradation_card = QFrame()
        degradation_card_layout = QVBoxLayout(degradation_card)

        degradation_label = QLabel("DEGRADATION RATE")
        degradation_label.setProperty("role", "metric_label")

        degradation_value = QLabel("2.8% / Year")
        degradation_value.setProperty("role", "metric")

        degradation_status = QLabel("Normal degradation")
        degradation_status.setProperty("role", "status")

        degradation_card_layout.addWidget(degradation_label)
        degradation_card_layout.addWidget(degradation_value)
        degradation_card_layout.addWidget(degradation_status)

        # ---------------------------------------------------------
        # Card Rows
        # ---------------------------------------------------------

        first_row = QHBoxLayout()
        first_row.addWidget(health_card)
        first_row.addWidget(rul_card)

        second_row = QHBoxLayout()
        second_row.addWidget(cycle_card)
        second_row.addWidget(degradation_card)

        # ---------------------------------------------------------
        # Add everything to dashboard
        # ---------------------------------------------------------

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addLayout(first_row)
        layout.addLayout(second_row)

        layout.addStretch()