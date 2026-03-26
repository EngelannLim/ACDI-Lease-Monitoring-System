import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction
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
    QToolButton,
    QMenu,
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
    # COMMON TOP BAR
    # =========================================================
    def create_top_bar(self, left_button_text, left_button_handler):
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        nav_btn = QPushButton(left_button_text)
        nav_btn.setMinimumHeight(40)
        nav_btn.clicked.connect(left_button_handler)

        settings_btn = QToolButton()
        settings_btn.setText("⚙")
        settings_btn.setObjectName("settingsButton")
        settings_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        settings_menu = QMenu(settings_btn)

        light_action = QAction("Light Mode", self)
        light_action.triggered.connect(lambda: self.apply_theme("light"))

        dark_action = QAction("Dark Mode", self)
        dark_action.triggered.connect(lambda: self.apply_theme("dark"))

        exit_action = QAction("Exit App", self)
        exit_action.triggered.connect(self.close)

        settings_menu.addAction(light_action)
        settings_menu.addAction(dark_action)
        settings_menu.addSeparator()
        settings_menu.addAction(exit_action)

        settings_btn.setMenu(settings_menu)

        top_bar.addWidget(nav_btn)
        top_bar.addStretch()
        top_bar.addWidget(settings_btn)

        return top_bar

    # =========================================================
    # MAIN PAGE
    # =========================================================
    def build_main_dashboard_page(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        root.addLayout(self.create_top_bar("Open Contract Expiry", self.show_expiry_page))

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

    # =========================================================
    # EXPIRY PAGE
    # =========================================================
    def build_contract_expiry_page(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        root.addLayout(self.create_top_bar("Back to Dashboard", self.show_main_page))

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
        table.setFrameShape(QTableWidget.Shape.NoFrame)

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
    # THEMES
    # =========================================================
    def apply_theme(self, theme):
        self.current_theme = theme
        if theme == "dark":
            self.setStyleSheet(self.dark_stylesheet())
        else:
            self.setStyleSheet(self.light_stylesheet())

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
            border: none;
            border-radius: 16px;
        }

        QLabel#companyLabel {
            font-size: 14px;
            font-weight: 700;
            color: #dbeafe;
            letter-spacing: 1px;
            background: transparent;
        }

        QLabel#pageTitle {
            font-size: 24px;
            font-weight: 800;
            color: white;
            background: transparent;
        }

        QLabel#subText {
            font-size: 13px;
            color: #e2e8f0;
            background: transparent;
        }

        QLabel#sectionLabel {
            font-size: 14px;
            font-weight: 700;
            color: #93c5fd;
            background: transparent;
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

        QToolButton#settingsButton {
            background-color: #1e293b;
            color: #f8fafc;
            border: none;
            border-radius: 18px;
            font-size: 18px;
            font-weight: 700;
            min-width: 38px;
            min-height: 38px;
            padding: 4px;
        }

        QToolButton#settingsButton:hover {
            background-color: #334155;
        }

        QMenu {
            background-color: #111827;
            color: #f8fafc;
            border: none;
            border-radius: 10px;
            padding: 8px;
        }

        QMenu::item {
            padding: 8px 22px 8px 12px;
            border-radius: 6px;
        }

        QMenu::item:selected {
            background-color: #1d4ed8;
        }

        QGroupBox {
            font-weight: 700;
            border: none;
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
            background: transparent;
        }

        QTableWidget {
            background-color: #111827;
            alternate-background-color: #172033;
            border: none;
            border-radius: 14px;
            color: #f8fafc;
            selection-background-color: #1d4ed8;
            selection-color: white;
            padding: 8px;
            outline: 0;
        }

        QHeaderView::section {
            background-color: #1e293b;
            color: #93c5fd;
            padding: 10px;
            border: none;
            font-weight: 800;
        }

        QTableWidget::item {
            padding: 8px;
            border: none;
        }

        QScrollBar:vertical {
            background: transparent;
            width: 10px;
            margin: 4px;
            border: none;
        }

        QScrollBar::handle:vertical {
            background: #334155;
            border-radius: 5px;
            min-height: 20px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0px;
        }

        QScrollBar:horizontal {
            background: transparent;
            height: 10px;
            margin: 4px;
            border: none;
        }

        QScrollBar::handle:horizontal {
            background: #334155;
            border-radius: 5px;
            min-width: 20px;
        }

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
            width: 0px;
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
            border: none;
            border-radius: 16px;
        }

        QLabel#companyLabel {
            font-size: 14px;
            font-weight: 700;
            color: #1e3a8a;
            letter-spacing: 1px;
            background: transparent;
        }

        QLabel#pageTitle {
            font-size: 24px;
            font-weight: 800;
            color: #082f49;
            background: transparent;
        }

        QLabel#subText {
            font-size: 13px;
            color: #334155;
            background: transparent;
        }

        QLabel#sectionLabel {
            font-size: 14px;
            font-weight: 700;
            color: #1d4ed8;
            background: transparent;
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

        QToolButton#settingsButton {
            background-color: #e2e8f0;
            color: #0f172a;
            border: none;
            border-radius: 18px;
            font-size: 18px;
            font-weight: 700;
            min-width: 38px;
            min-height: 38px;
            padding: 4px;
        }

        QToolButton#settingsButton:hover {
            background-color: #cbd5e1;
        }

        QMenu {
            background-color: white;
            color: #0f172a;
            border: none;
            border-radius: 10px;
            padding: 8px;
        }

        QMenu::item {
            padding: 8px 22px 8px 12px;
            border-radius: 6px;
        }

        QMenu::item:selected {
            background-color: #dbeafe;
        }

        QGroupBox {
            font-weight: 700;
            border: none;
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
            background: transparent;
        }

        QTableWidget {
            background-color: white;
            alternate-background-color: #f1f5f9;
            border: none;
            border-radius: 14px;
            color: #0f172a;
            selection-background-color: #bfdbfe;
            selection-color: #0f172a;
            padding: 8px;
            outline: 0;
        }

        QHeaderView::section {
            background-color: #e2e8f0;
            color: #1e3a8a;
            padding: 10px;
            border: none;
            font-weight: 800;
        }

        QTableWidget::item {
            padding: 8px;
            border: none;
        }

        QScrollBar:vertical {
            background: transparent;
            width: 10px;
            margin: 4px;
            border: none;
        }

        QScrollBar::handle:vertical {
            background: #94a3b8;
            border-radius: 5px;
            min-height: 20px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0px;
        }

        QScrollBar:horizontal {
            background: transparent;
            height: 10px;
            margin: 4px;
            border: none;
        }

        QScrollBar::handle:horizontal {
            background: #94a3b8;
            border-radius: 5px;
            min-width: 20px;
        }

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
            width: 0px;
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