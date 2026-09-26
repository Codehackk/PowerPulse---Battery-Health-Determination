from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Battery Overview")
        subtitle = QLabel(
            "Monitor battery health, degradation, and lifecycle status."
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()