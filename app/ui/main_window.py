from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

from app.core.config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from app.views.dashboard import DashboardView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Main application container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QVBoxLayout()

        logo = QLabel("POWERPULSE")
        sidebar.addWidget(logo)

        dashboard_button = QPushButton("Dashboard")
        diagnostics_button = QPushButton("Diagnostics")
        rul_button = QPushButton("RUL Analysis")
        valuation_button = QPushButton("Valuation")
        second_life_button = QPushButton("Second Life")
        vendors_button = QPushButton("Vendors")
        reports_button = QPushButton("Reports")
        settings_button = QPushButton("Settings")

        sidebar.addWidget(dashboard_button)
        sidebar.addWidget(diagnostics_button)
        sidebar.addWidget(rul_button)
        sidebar.addWidget(valuation_button)
        sidebar.addWidget(second_life_button)
        sidebar.addWidget(vendors_button)
        sidebar.addWidget(reports_button)

        sidebar.addStretch()

        sidebar.addWidget(settings_button)

        # Main content
        content = QVBoxLayout()

        dashboard = DashboardView()
        content.addWidget(dashboard)

        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(content, 4)