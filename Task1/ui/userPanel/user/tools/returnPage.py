from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QHeaderView
)

class ReturnPage(QWidget):
    def __init__(self):
        super().__init__()
        self.build_return_page()
    
    def build_return_page(self) -> QWidget:
        self.return_page = QFrame()
        self.return_page.setObjectName("card")
        self.return_layout = QVBoxLayout(self.return_page)
        self.init_return_title()
        self.init_return_table()
        # Add inner frame to this QWidget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.return_page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        return self.return_page
    
    def init_return_title(self) -> None:
        self.return_title = QLabel("Return Books")
        self.return_title.setObjectName("title")
        self.return_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_layout.addWidget(self.return_title)
    
    def init_return_table(self) -> None:
        self.return_table = QTableWidget(0, 3)
        self.return_table.setHorizontalHeaderLabels(["Due Date", "Book", "Action"])
        self.return_table.verticalHeader().setVisible(False)
        self.return_header = self.return_table.horizontalHeader()
        self.return_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.return_header.setStretchLastSection(True)
        self.return_table.setColumnWidth(0, 170)
        self.return_table.setColumnWidth(1, 400)
        self.return_layout.addWidget(self.return_table)