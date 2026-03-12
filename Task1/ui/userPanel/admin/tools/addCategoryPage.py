from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QMessageBox,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)

from PySide6.QtCore import Qt
from ui.userPanel.admin.tools.abstractPage import AbstractPage

class AddCategoryPage(AbstractPage):
    def __init__(self, on_refresh) -> None:
        super().__init__()
        self.on_refresh = on_refresh
        self.init_add_category_page()
        self.init_add_category_layout()
        self.init_add_category_title()
        self.init_add_category_row()
        self.init_add_category_button()
        self.init_add_category_page_layout()

    def init_add_category_page(self) -> None:
        self.add_category_page = QFrame()
        self.add_category_page.setObjectName("card")
        # Set up main layout for this widget
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.add_category_page)

    def init_add_category_layout(self) -> None:
        self.add_category_layout = QVBoxLayout(self.add_category_page)
        self.add_category_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

    def init_add_category_title(self) -> None:
        self.add_category_title = QLabel("Add Category")
        self.add_category_title.setObjectName("title")
        self.add_category_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_category_layout.addWidget(self.add_category_title)

    def init_add_category_row(self) -> None:
        self.add_category_row = QHBoxLayout()
        self.new_category_input = QLineEdit()
        self.new_category_input.setPlaceholderText("New category name")
        self.new_category_input.setMaximumWidth(320)
        self.add_category_row.addWidget(self.new_category_input)

    def init_add_category_button(self) -> None:

        self.add_category_button = QPushButton("Add Category")
        self.add_category_button.clicked.connect(self.add_category)
        self.add_category_row.addWidget(self.add_category_button)
        self.add_category_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def init_add_category_page_layout(self) -> None:
        self.add_category_layout.addLayout(self.add_category_row)
        self.add_category_layout.addStretch(1)

    def add_category(self) -> None:
        category = self.new_category_input.text().strip()
        try:
            created = self.admin_service.add_category(category)
        except ValueError as error:
            QMessageBox.warning(self, "Add Category Failed", str(error))
            return
        QMessageBox.information(self, "Add Category", f"Category added: {created}")
        self.new_category_input.clear()
        self.on_refresh()