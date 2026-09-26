from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from app.core.vendors import (
    get_demo_vendors,
    search_vendors,
)


class VendorsView(QWidget):
    def __init__(self):
        super().__init__()

        self.vendors = get_demo_vendors()

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

            QPushButton#search_button {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#search_button:hover {
                background-color: #1d4ed8;
            }

            QLabel[role="hint"] {
                color: #64748b;
                font-size: 12px;
            }

            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #e2e8f0;
                font-size: 13px;
            }

            QTableWidget::item {
                padding: 8px;
            }

            QHeaderView::section {
                background-color: #f8fafc;
                color: #475569;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                padding: 10px;
                font-size: 11px;
                font-weight: 600;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # ---------------------------------------------------------
        # Page heading
        # ---------------------------------------------------------

        title = QLabel("Vendors")
        title.setProperty("role", "title")

        subtitle = QLabel(
            "Browse prototype vendors for battery-related "
            "services and second-life applications."
        )
        subtitle.setProperty("role", "subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------------------------------------------------------
        # Search card
        # ---------------------------------------------------------

        search_card = QFrame()
        search_card.setProperty("role", "card")

        search_layout = QVBoxLayout(search_card)

        search_row = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by vendor, service, specialization, or location..."
        )

        search_button = QPushButton("Search")
        search_button.setObjectName("search_button")

        search_row.addWidget(self.search_input)
        search_row.addWidget(search_button)

        search_layout.addLayout(search_row)

        hint = QLabel(
            "Prototype vendor data is used for this version."
        )
        hint.setProperty("role", "hint")

        search_layout.addWidget(hint)

        layout.addWidget(search_card)

        # ---------------------------------------------------------
        # Vendor table
        # ---------------------------------------------------------

        table_card = QFrame()
        table_card.setProperty("role", "card")

        table_layout = QVBoxLayout(table_card)

        self.vendor_table = QTableWidget()

        self.vendor_table.setColumnCount(6)

        self.vendor_table.setHorizontalHeaderLabels([
            "Vendor",
            "Service",
            "Specialization",
            "Location",
            "Contact",
            "Status",
        ])

        self.vendor_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.vendor_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.vendor_table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.vendor_table.verticalHeader().setVisible(
            False
        )

        header = self.vendor_table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.Stretch
        )

        table_layout.addWidget(
            self.vendor_table
        )

        layout.addWidget(table_card)

        layout.addStretch()

        # ---------------------------------------------------------
        # Search connections
        # ---------------------------------------------------------

        search_button.clicked.connect(
            self.search
        )

        self.search_input.returnPressed.connect(
            self.search
        )

        # ---------------------------------------------------------
        # Initial data
        # ---------------------------------------------------------

        self.populate_table(self.vendors)

    def populate_table(self, vendors):
        """Populate the vendor table."""

        self.vendor_table.setRowCount(
            len(vendors)
        )

        for row, vendor in enumerate(vendors):

            data = vendor.to_dict()

            values = [
                data["name"],
                data["service_type"],
                data["specialization"],
                data["location"],
                data["contact"],
                data["status"],
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(
                    str(value)
                )

                self.vendor_table.setItem(
                    row,
                    column,
                    item,
                )

    def search(self):
        """Search the vendor directory."""

        search_term = (
            self.search_input.text()
        )

        results = search_vendors(
            self.vendors,
            search_term,
        )

        self.populate_table(results)