import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QGroupBox,
    QGridLayout,
    QStackedWidget,
    QHeaderView,
    QAbstractItemView,
    QSizePolicy,
    QFrame,
)

from shared_data import store


class LeaseMonitoringWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ACDI Lease Monitoring System")
        self.resize(1800, 900)

        self.current_theme = "dark"

        self.stacked = QStackedWidget()

        self.main_page = self.build_main_dashboard_page()
        self.expiry_page = self.build_contract_expiry_page()

        self.stacked.addWidget(self.main_page)
        self.stacked.addWidget(self.expiry_page)

        self.setCentralWidget(self.stacked)
        self.apply_theme(self.current_theme)

    # =========================================================
    # PAGE BUILDERS
    # =========================================================
    def build_main_dashboard_page(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.expiry_btn = QPushButton("Open Contract Expiry")
        self.expiry_btn.setMinimumHeight(42)
        self.expiry_btn.clicked.connect(self.show_expiry_page)

        self.theme_btn_1 = QPushButton("Switch to Light Mode")
        self.theme_btn_1.setMinimumHeight(42)
        self.theme_btn_1.clicked.connect(self.toggle_theme)

        top_bar.addWidget(self.expiry_btn)
        top_bar.addWidget(self.theme_btn_1)
        top_bar.addStretch()

        root.addLayout(top_bar)

        # Header card
        header_card = QFrame()
        header_card.setObjectName("headerCard")
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(20, 18, 20, 18)
        header_layout.setSpacing(6)

        company = QLabel("VISMIN LENDING GROUP")
        company.setObjectName("companyLabel")

        subtitle = QLabel("STATUS OF LEASE CONTRACT")
        subtitle.setObjectName("pageTitle")

        description = QLabel(
            "Track lease contract movement, routing progress, and approval status across offices."
        )
        description.setObjectName("subText")
        description.setWordWrap(True)

        header_layout.addWidget(company)
        header_layout.addWidget(subtitle)
        header_layout.addWidget(description)

        root.addWidget(header_card)

        # Main table
        self.main_table = QTableWidget()
        main_headers = [
            "DATE RECEIVED",
            "TITLE",
            "RS No.",
            "GSS MEMO No.",
            "LEGAL",
            "VLG H",
            "GSD",
            "AD",
            "OD",
            "VP-ASSIGNED OTD",
            "EVPO-EVPA",
            "PRESIDENT(GLOBODOX)",
            "REMARKS",
        ]
        main_widths = [130, 560, 80, 105, 90, 90, 120, 80, 80, 110, 100, 130, 450]

        self.configure_table(
            table=self.main_table,
            headers=main_headers,
            widths=main_widths,
            rows=store.get_main_dashboard_rows(),
            row_height=32,
            fixed_resize=False,
        )

        root.addWidget(self.main_table)

        footer_box = QGroupBox("LEASE CONTRACT ROUTING PROCESS (HEAD OFFICE)")
        footer_box.setObjectName("infoBox")
        footer_layout = QVBoxLayout(footer_box)

        note_title = QLabel("NOTE")
        note_title.setObjectName("sectionLabel")

        note_text = QLabel(
            "Once the branch sends the request (renewal, extension, new contract, etc.), "
            "the document is routed to the Head Office for review and approval in sequence. "
            "Each office indicates completion before forwarding the document to the next office "
            "until final approval is obtained."
        )
        note_text.setWordWrap(True)
        note_text.setObjectName("subText")

        footer_layout.addWidget(note_title)
        footer_layout.addWidget(note_text)

        root.addWidget(footer_box)
        return page

    def build_contract_expiry_page(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.back_btn = QPushButton("Back to Dashboard")
        self.back_btn.setMinimumHeight(42)
        self.back_btn.clicked.connect(self.show_main_page)

        self.theme_btn_2 = QPushButton("Switch to Light Mode")
        self.theme_btn_2.setMinimumHeight(42)
        self.theme_btn_2.clicked.connect(self.toggle_theme)

        top_bar.addWidget(self.back_btn)
        top_bar.addWidget(self.theme_btn_2)
        top_bar.addStretch()

        root.addLayout(top_bar)

        # Title + legend row
        info_row = QHBoxLayout()
        info_row.setSpacing(14)

        title_card = QFrame()
        title_card.setObjectName("headerCard")
        title_layout = QVBoxLayout(title_card)
        title_layout.setContentsMargins(20, 18, 20, 18)

        title = QLabel("CONTRACT EXPIRY")
        title.setObjectName("pageTitle")

        desc = QLabel(
            "Monitor branches with active lease terms, deadline reminders, and completion updates."
        )
        desc.setObjectName("subText")
        desc.setWordWrap(True)

        title_layout.addWidget(title)
        title_layout.addWidget(desc)

        legend_group = QGroupBox("LEGEND")
        legend_group.setObjectName("legendBox")
        legend_layout = QGridLayout(legend_group)

        for row_index, (count, text) in enumerate(store.get_legend_rows()):
            count_label = QLabel(str(count))
            count_label.setObjectName("legendCount")
            text_label = QLabel(text)
            text_label.setObjectName("legendText")
            legend_layout.addWidget(count_label, row_index, 0)
            legend_layout.addWidget(text_label, row_index, 1)

        info_row.addWidget(title_card, 3)
        info_row.addWidget(legend_group, 2)

        root.addLayout(info_row)

        self.expiry_table = QTableWidget()
        expiry_headers = [
            "BRANCH",
            "DATE RECEIVED",
            "DATE SENT\nTO HO",
            "TERM",
            "HEAD",
            "HEAD CONTACT NO.",
            "REMINDER\n(2 mos before deadline)",
            "FROM",
            "TO",
            "FLOOR AREA",
            "MEMO #",
            "DATE COMPLETED\n/SENT",
            "REMARKS",
        ]
        expiry_widths = [180, 90, 95, 140, 150, 120, 100, 75, 75, 80, 180, 105, 300]

        self.configure_table(
            table=self.expiry_table,
            headers=expiry_headers,
            widths=expiry_widths,
            rows=store.get_expiry_rows(),
            row_height=32,
            fixed_resize=True,
        )

        root.addWidget(self.expiry_table)
        return page

    # =========================================================
    # TABLE SETUP
    # =========================================================
    def configure_table(self, table, headers, widths, rows, row_height=32, fixed_resize=False):
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(rows))

        table.verticalHeader().setVisible(False)
        table.setWordWrap(True)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if fixed_resize:
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        else:
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        for index, width in enumerate(widths):
            table.setColumnWidth(index, width)

        for row_index, row_data in enumerate(rows):
            table.setRowHeight(row_index, row_height)
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                table.setItem(row_index, col_index, item)

        table.horizontalHeader().setStretchLastSection(False)

    # =========================================================
    # THEME CONTROL
    # =========================================================
    def toggle_theme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
        else:
            self.current_theme = "dark"

        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet(self.dark_stylesheet())
            self.theme_btn_1.setText("Switch to Light Mode")
            self.theme_btn_2.setText("Switch to Light Mode")
        else:
            self.setStyleSheet(self.light_stylesheet())
            self.theme_btn_1.setText("Switch to Dark Mode")
            self.theme_btn_2.setText("Switch to Dark Mode")

    def dark_stylesheet(self):
        return """
        QMainWindow, QWidget {
            background-color: #0f172a;
            color: #e2e8f0;
            font-family: Segoe UI, Arial, sans-serif;
            font-size: 13px;
        }

        QFrame#headerCard {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #1d4ed8,
                stop:1 #0f766e
            );
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        QLabel#companyLabel {
            font-size: 14px;
            font-weight: 700;
            color: #dbeafe;
            letter-spacing: 1px;
        }

        QLabel#pageTitle {
            font-size: 24px;
            font-weight: 800;
            color: white;
        }

        QLabel#subText {
            font-size: 13px;
            color: #e2e8f0;
        }

        QLabel#sectionLabel {
            font-size: 14px;
            font-weight: 700;
            color: #93c5fd;
        }

        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 16px;
            font-weight: 700;
        }

        QPushButton:hover {
            background-color: #3b82f6;
        }

        QPushButton:pressed {
            background-color: #1d4ed8;
        }

        QGroupBox {
            font-weight: 700;
            border: 1px solid #334155;
            border-radius: 14px;
            margin-top: 12px;
            padding-top: 12px;
            background-color: #111827;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 14px;
            padding: 0 6px 0 6px;
            color: #93c5fd;
        }

        QGroupBox#infoBox,
        QGroupBox#legendBox {
            background-color: #111827;
        }

        QLabel#legendCount {
            background-color: #1d4ed8;
            color: white;
            border-radius: 10px;
            padding: 6px 10px;
            font-weight: 800;
            min-width: 24px;
        }

        QLabel#legendText {
            color: #e5e7eb;
            padding-left: 4px;
        }

        QTableWidget {
            background-color: #111827;
            alternate-background-color: #172033;
            border: 1px solid #334155;
            border-radius: 14px;
            gridline-color: #334155;
            color: #f8fafc;
            selection-background-color: #1d4ed8;
            selection-color: white;
            padding: 8px;
        }

        QHeaderView::section {
            background-color: #1e293b;
            color: #93c5fd;
            padding: 10px;
            border: none;
            border-bottom: 1px solid #334155;
            font-weight: 800;
        }

        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #1f2937;
        }

        QScrollBar:vertical {
            background: #0f172a;
            width: 12px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #334155;
            border-radius: 6px;
            min-height: 20px;
        }

        QScrollBar:horizontal {
            background: #0f172a;
            height: 12px;
            margin: 0px;
        }

        QScrollBar::handle:horizontal {
            background: #334155;
            border-radius: 6px;
            min-width: 20px;
        }
        """

    def light_stylesheet(self):
        return """
        QMainWindow, QWidget {
            background-color: #f8fafc;
            color: #0f172a;
            font-family: Segoe UI, Arial, sans-serif;
            font-size: 13px;
        }

        QFrame#headerCard {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #60a5fa,
                stop:1 #2dd4bf
            );
            border-radius: 16px;
            border: 1px solid #cbd5e1;
        }

        QLabel#companyLabel {
            font-size: 14px;
            font-weight: 700;
            color: #1e3a8a;
            letter-spacing: 1px;
        }

        QLabel#pageTitle {
            font-size: 24px;
            font-weight: 800;
            color: #082f49;
        }

        QLabel#subText {
            font-size: 13px;
            color: #334155;
        }

        QLabel#sectionLabel {
            font-size: 14px;
            font-weight: 700;
            color: #1d4ed8;
        }

        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 16px;
            font-weight: 700;
        }

        QPushButton:hover {
            background-color: #3b82f6;
        }

        QPushButton:pressed {
            background-color: #1d4ed8;
        }

        QGroupBox {
            font-weight: 700;
            border: 1px solid #cbd5e1;
            border-radius: 14px;
            margin-top: 12px;
            padding-top: 12px;
            background-color: white;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 14px;
            padding: 0 6px 0 6px;
            color: #1d4ed8;
        }

        QLabel#legendCount {
            background-color: #dbeafe;
            color: #1d4ed8;
            border-radius: 10px;
            padding: 6px 10px;
            font-weight: 800;
            min-width: 24px;
        }

        QLabel#legendText {
            color: #334155;
            padding-left: 4px;
        }

        QTableWidget {
            background-color: white;
            alternate-background-color: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-radius: 14px;
            gridline-color: #e2e8f0;
            color: #0f172a;
            selection-background-color: #bfdbfe;
            selection-color: #0f172a;
            padding: 8px;
        }

        QHeaderView::section {
            background-color: #e2e8f0;
            color: #1e3a8a;
            padding: 10px;
            border: none;
            border-bottom: 1px solid #cbd5e1;
            font-weight: 800;
        }

        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #e5e7eb;
        }

        QScrollBar:vertical {
            background: #e2e8f0;
            width: 12px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #94a3b8;
            border-radius: 6px;
            min-height: 20px;
        }

        QScrollBar:horizontal {
            background: #e2e8f0;
            height: 12px;
            margin: 0px;
        }

        QScrollBar::handle:horizontal {
            background: #94a3b8;
            border-radius: 6px;
            min-width: 20px;
        }
        """

    # =========================================================
    # PAGE SWITCHING
    # =========================================================
    def show_expiry_page(self):
        self.stacked.setCurrentWidget(self.expiry_page)

    def show_main_page(self):
        self.stacked.setCurrentWidget(self.main_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LeaseMonitoringWindow()
    window.show()
    sys.exit(app.exec())