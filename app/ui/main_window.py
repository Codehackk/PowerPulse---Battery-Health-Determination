from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget,
)

from app.core.config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from app.views.dashboard import DashboardView
from app.diagnostics import DiagnosticsView
from app.views.rul_analysis import RULAnalysisView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f7fb;
            }

            QWidget {
                font-family: "Segoe UI";
            }

            #sidebar {
                background-color: #111827;
            }

            #brand {
                color: white;
                font-size: 22px;
                font-weight: 700;
                padding: 8px 4px;
            }

            #brand_subtitle {
                color: #94a3b8;
                font-size: 11px;
                padding: 0 4px 20px 4px;
            }

            QPushButton {
                background-color: transparent;
                color: #cbd5e1;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding: 12px 14px;
                font-size: 13px;
                font-weight: 500;
            }

            QPushButton:hover {
                background-color: #1f2937;
                color: white;
            }

            QPushButton:pressed {
                background-color: #273449;
            }

            QPushButton#active_button {
                background-color: #2563eb;
                color: white;
                font-weight: 600;
            }

            #content_area {
                background-color: #f4f7fb;
            }
        """)

        # ---------------------------------------------------------
        # Main application container
        # ---------------------------------------------------------

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------------------------------------------------
        # Sidebar
        # ---------------------------------------------------------

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 24, 18, 18)
        sidebar_layout.setSpacing(6)

        # Branding
        logo = QLabel("POWERPULSE")
        logo.setObjectName("brand")

        brand_subtitle = QLabel(
            "Battery Intelligence Platform"
        )
        brand_subtitle.setObjectName(
            "brand_subtitle"
        )

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(brand_subtitle)

        # Navigation buttons
        dashboard_button = QPushButton("Dashboard")
        diagnostics_button = QPushButton("Diagnostics")
        rul_button = QPushButton("RUL Analysis")
        valuation_button = QPushButton("Valuation")
        second_life_button = QPushButton("Second Life")
        vendors_button = QPushButton("Vendors")
        reports_button = QPushButton("Reports")

        dashboard_button.setObjectName(
            "active_button"
        )

        sidebar_layout.addWidget(
            dashboard_button
        )

        sidebar_layout.addWidget(
            diagnostics_button
        )

        sidebar_layout.addWidget(
            rul_button
        )

        sidebar_layout.addWidget(
            valuation_button
        )

        sidebar_layout.addWidget(
            second_life_button
        )

        sidebar_layout.addWidget(
            vendors_button
        )

        sidebar_layout.addWidget(
            reports_button
        )

        sidebar_layout.addStretch()

        settings_button = QPushButton("Settings")

        sidebar_layout.addWidget(
            settings_button
        )

        # ---------------------------------------------------------
        # Content area
        # ---------------------------------------------------------

        content_area = QFrame()
        content_area.setObjectName(
            "content_area"
        )

        content_layout = QVBoxLayout(
            content_area
        )

        content_layout.setContentsMargins(
            28,
            28,
            28,
            28,
        )

        content_layout.setSpacing(0)

        # ---------------------------------------------------------
        # Page stack
        # ---------------------------------------------------------

        pages = QStackedWidget()

        dashboard = DashboardView()
        diagnostics = DiagnosticsView()
        rul_analysis = RULAnalysisView()

        pages.addWidget(dashboard)
        pages.addWidget(diagnostics)
        pages.addWidget(rul_analysis)

        content_layout.addWidget(pages)

        # ---------------------------------------------------------
        # Navigation helper
        # ---------------------------------------------------------

        buttons = [
            dashboard_button,
            diagnostics_button,
            rul_button,
        ]

        def set_active_button(active_button):
            for button in buttons:
                button.setObjectName("")

            active_button.setObjectName(
                "active_button"
            )

            for button in buttons:
                button.style().unpolish(button)
                button.style().polish(button)
                button.update()

        # ---------------------------------------------------------
        # Page navigation
        # ---------------------------------------------------------

        def show_dashboard():
            pages.setCurrentWidget(
                dashboard
            )

            set_active_button(
                dashboard_button
            )

        def show_diagnostics():
            pages.setCurrentWidget(
                diagnostics
            )

            set_active_button(
                diagnostics_button
            )

        def show_rul_analysis():
            pages.setCurrentWidget(
                rul_analysis
            )

            set_active_button(
                rul_button
            )

        dashboard_button.clicked.connect(
            show_dashboard
        )

        diagnostics_button.clicked.connect(
            show_diagnostics
        )

        rul_button.clicked.connect(
            show_rul_analysis
        )

        # ---------------------------------------------------------
        # Final layout
        # ---------------------------------------------------------

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)