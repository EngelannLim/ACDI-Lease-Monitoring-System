from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from shared_data import store


class ContractExpiryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contract Expiry")
        self.resize(1700, 850)

        self.table = None
        self.legend_group = None

        self.build_ui()
        self.load_data()

    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(10)

        top_row = QHBoxLayout()

        title = QLabel("CONTRACT EXPIRY")
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        title.setFont(font)
        top_row.addWidget(title)
        top_row.addStretch()

        self.legend_group = QGroupBox("LEGEND")
        legend_layout = QGridLayout(self.legend_group)
        legend_layout.setContentsMargins(8, 8, 8, 8)
        legend_layout.setHorizontalSpacing(10)
        legend_layout.setVerticalSpacing(4)
        top_row.addWidget(self.legend_group)

        root.addLayout(top_row)

        self.table = QTableWidget()
        headers = [
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
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setWordWrap(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        widths = [180, 90, 95, 140, 150, 120, 100, 75, 75, 80, 180, 105, 300]
        for i, w in enumerate(widths):
            self.table.setColumnWidth(i, w)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        root.addWidget(self.table)

    def load_data(self):
        self.load_legend()
        rows = store.get_expiry_rows()
        self.table.setRowCount(len(rows))

        for r in range(len(rows)):
            self.table.setRowHeight(r, 28)

        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_idx, col_idx, item)

    def load_legend(self):
        layout = self.legend_group.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        legend_rows = store.get_legend_rows()
        for i, (count, text) in enumerate(legend_rows):
            layout.addWidget(QLabel(count), i, 0)
            layout.addWidget(QLabel(text), i, 1)

    def refresh_data(self):
        self.load_data()