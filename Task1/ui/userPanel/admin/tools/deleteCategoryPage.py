from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QHeaderView,
    QMessageBox,
    QAbstractItemView
)

from PySide6.QtCore import Qt
from ui.userPanel.admin.tools.abstractPage import AbstractPage

class DeleteCategoryPage(AbstractPage):
    def __init__(self, on_refresh) -> None:
        super().__init__()
        self.on_refresh = on_refresh
        self.init_delete_category_page()
        self.init_delete_category_layout()
        self.init_delete_category_title()
        self.init_delete_category_table()

    def init_delete_category_page(self) -> None:
        self.delete_category_page = QFrame()
        self.delete_category_page.setObjectName("card")
        # Set up main layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.delete_category_page)

    def init_delete_category_layout(self) -> None:
        self.delete_category_layout = QVBoxLayout(self.delete_category_page)
        self.delete_category_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def init_delete_category_title(self) -> None:
        self.delete_category_title = QLabel("Delete Category")
        self.delete_category_title.setObjectName("title")
        self.delete_category_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.delete_category_layout.addWidget(self.delete_category_title)

    def init_delete_category_table(self) -> None:
        self.delete_category_table = QTableWidget(0, 2)
        self.delete_category_table.setHorizontalHeaderLabels(["Category", "Action"])
        self.delete_category_table.verticalHeader().setVisible(False)
        self.delete_category_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.delete_category_table.setMinimumWidth(520)
        # Disable editing
        self.delete_category_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.delete_category_layout.addWidget(self.delete_category_table)
        self.delete_category_layout.addStretch(1)
    
    def delete_category(self, category: str) -> None:
        if not self.common_function.confirm_action(
            self, "Confirm Delete Category", f"Delete category '{category}' permanently?"
        ):
            return
        try:
            deleted = self.admin_service.delete_category(category)
        except ValueError as error:
            QMessageBox.warning(self, "Delete Category Failed", str(error))
            return
        QMessageBox.information(self, "Delete Category", f"Deleted category: {deleted}")
        self.on_refresh()
