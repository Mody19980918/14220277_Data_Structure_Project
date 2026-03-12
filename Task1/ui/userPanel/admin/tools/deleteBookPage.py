from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QHeaderView,
    QMessageBox,
    QAbstractItemView
)

from PySide6.QtCore import Qt
from ui.userPanel.admin.tools.abstractPage import AbstractPage

class DeleteBookPage(AbstractPage):
    def __init__(self, on_refresh_categories, on_refresh_delete_book_categories, on_refresh_books_for_category) -> None:
        super().__init__()
        self.on_refresh_categories = on_refresh_categories
        self.on_refresh_delete_book_categories = on_refresh_delete_book_categories
        self.on_refresh_books_for_category = on_refresh_books_for_category
        self.init_delete_book_page()
        self.init_delete_book_layout()
        self.init_delete_book_title()
        self.init_delete_book_category_select()
        self.init_delete_book_table()

    def refresh_delete_books_for_category(self, category: str) -> None:
        """Refresh books when category changes"""
        if category and self.on_refresh_books_for_category:
            self.on_refresh_books_for_category(category)

    def init_delete_book_page(self) -> None:
        self.delete_book_page = QFrame()
        self.delete_book_page.setObjectName("card")
        # Set up main layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.delete_book_page)

    def init_delete_book_layout(self) -> None:
        self.delete_book_layout = QVBoxLayout(self.delete_book_page)
        self.delete_book_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def init_delete_book_title(self) -> None:
        self.delete_book_title = QLabel("Delete Book")
        self.delete_book_title.setObjectName("title")
        self.delete_book_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.delete_book_layout.addWidget(self.delete_book_title)


    def init_delete_book_category_select(self) -> None:

        self.delete_book_category_select = QComboBox()
        self.delete_book_category_select.setMinimumWidth(320)
        self.delete_book_category_select.currentTextChanged.connect(
            self.refresh_delete_books_for_category
        )
        self.delete_book_layout.addWidget(self.delete_book_category_select)

    def init_delete_book_table(self) -> None:
        self.delete_book_table = QTableWidget(0, 2)
        self.delete_book_table.setHorizontalHeaderLabels(["Book", "Action"])
        self.delete_book_table.verticalHeader().setVisible(False)
        self.delete_book_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.delete_book_table.setMinimumWidth(520)
        # Disable editing
        self.delete_book_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.delete_book_layout.addWidget(self.delete_book_table)
        self.delete_book_layout.addStretch(1)

    def delete_book(self, book_name: str) -> None:
        if not self.common_function.confirm_action(
            self, "Confirm Delete Book", f"Delete book '{book_name}' permanently?"
        ):
            return
        try:
            deleted = self.admin_service.delete_book(book_name)
        except ValueError as error:
            QMessageBox.warning(self, "Delete Book Failed", str(error))
            return
        QMessageBox.information(self, "Delete Book", f"Deleted book: {deleted}")
        self.on_refresh_delete_book_categories()
        self.on_refresh_categories()
