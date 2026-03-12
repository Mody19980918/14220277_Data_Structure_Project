from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QTableWidget,
    QHeaderView,
    QAbstractItemView
)

class BorrowPage(QWidget):
    def __init__(self, on_category_changed=None):
        super().__init__()
        self.on_category_changed = on_category_changed
        self.build_borrow_page()

    def build_borrow_page(self) -> QWidget:
        self.borrow_page = QFrame()
        self.borrow_page.setObjectName("card")
        self.borrow_layout = QVBoxLayout(self.borrow_page)
        self.init_borrow_title()
        self.init_category_combo()
        self.init_borrow_table()
        # Add inner frame to this QWidget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.borrow_page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        return self.borrow_page

    def init_borrow_title(self) -> None:
        self.borrow_title = QLabel("Borrow Books")
        self.borrow_title.setObjectName("title")
        self.borrow_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.borrow_layout.addWidget(self.borrow_title)

    def init_category_combo(self) -> None:
        self.category_combo = QComboBox()
        if self.on_category_changed:
            self.category_combo.currentTextChanged.connect(self.on_category_changed)
        self.borrow_layout.addWidget(self.category_combo)

    def init_borrow_table(self) -> None:
        self.borrow_table = QTableWidget(0, 3)
        self.borrow_table.setHorizontalHeaderLabels(["Category", "Book", "Action"])
        self.borrow_table.verticalHeader().setVisible(False)
        self.borrow_header = self.borrow_table.horizontalHeader()
        self.borrow_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.borrow_header.setStretchLastSection(True)
        self.borrow_table.setColumnWidth(0, 140)
        self.borrow_table.setColumnWidth(1, 430)
        # Disable editing
        self.borrow_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.borrow_layout.addWidget(self.borrow_table)
