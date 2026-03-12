from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QAbstractItemView
)   

from PySide6.QtCore import Qt
from ui.userPanel.admin.tools.abstractPage import AbstractPage


class DeleteUserPage(AbstractPage):
    def __init__(self, on_refresh) -> None:
        super().__init__()
        self.on_refresh = on_refresh
        self.init_delete_user_page()
        self.init_delete_user_layout()
        self.init_delete_user_title()
        self.init_delete_user_search_row()
        self.init_delete_user_result_label()
        self.init_delete_user_table()
        self.init_delete_user_button()

    def init_delete_user_page(self) -> None:
        self.delete_user_page = QFrame()
        self.delete_user_page.setObjectName("card")
        # Set up main layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.delete_user_page)

    def init_delete_user_layout(self) -> None:
        self.delete_user_layout = QVBoxLayout(self.delete_user_page)
        self.delete_user_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def init_delete_user_title(self) -> None:
        self.delete_user_title = QLabel("Delete User Account")
        self.delete_user_title.setObjectName("title")
        self.delete_user_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.delete_user_layout.addWidget(self.delete_user_title)

    def init_delete_user_search_row(self) -> None:
        self.delete_user_search_row = QHBoxLayout()
        self.delete_user_search_input = QLineEdit()
        self.delete_user_search_input.setPlaceholderText("Search username")
        self.delete_user_search_row.addWidget(self.delete_user_search_input)
        self.delete_user_search_button = QPushButton("Search")
        self.delete_user_search_button.clicked.connect(self.search_delete_user)
        self.delete_user_search_row.addWidget(self.delete_user_search_button)
        self.delete_user_layout.addLayout(self.delete_user_search_row)

    def init_delete_user_result_label(self) -> None:
        self.delete_user_result_label = QLabel("No result yet.")
        self.delete_user_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.delete_user_layout.addWidget(self.delete_user_result_label)

    def init_delete_user_table(self) -> None:
        self.delete_user_table = QTableWidget(1, 2)
        self.delete_user_table.setHorizontalHeaderLabels(["Username", "Role"])
        self.delete_user_table.verticalHeader().setVisible(False)
        self.delete_user_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.delete_user_table.setVisible(False)
        self.delete_user_table.setMinimumWidth(520)
        # Disable editing
        self.delete_user_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.delete_user_layout.addWidget(self.delete_user_table)

    def init_delete_user_button(self) -> None:
        self.delete_user_button = QPushButton("Delete User")
        self.delete_user_button.setVisible(False)
        self.delete_user_button.clicked.connect(self.delete_user)
        self.delete_user_layout.addWidget(self.delete_user_button)
        self.delete_user_layout.addStretch(1)

    def search_delete_user(self) -> None:
        username = self.delete_user_search_input.text().strip()
        if not username:
            self.delete_user_result_label.setText("User not found")
            self.delete_user_table.setVisible(False)
            self.delete_user_button.setVisible(False)
            return
        users = self.admin_service.list_deletable_usernames()
        if username not in users:
            self.delete_user_result_label.setText("User not found")
            self.delete_user_table.setVisible(False)
            self.delete_user_button.setVisible(False)
            return
        self.delete_user_result_label.setText("")
        self.set_delete_user_row(username, "user")
        self.delete_user_table.setVisible(True)
        self.delete_user_button.setVisible(True)
    
    
    def set_delete_user_row(self, username: str, role: str) -> None:
        username_item = QTableWidgetItem(username)
        role_item = QTableWidgetItem(role)
        username_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.delete_user_table.setItem(0, 0, username_item)
        self.delete_user_table.setItem(0, 1, role_item)

    def delete_user(self) -> None:
        username_item = self.delete_user_table.item(0, 0)
        username = username_item.text().strip() if username_item else ""
        if not username:
            QMessageBox.warning(self, "Delete User", "Please search user first.")
            return
        if not self.common_function.confirm_action(
            self, "Confirm Delete User", f"Delete user account '{username}' permanently?"
        ):
            return
        try:
            deleted = self.admin_service.delete_user_account(username)
        except ValueError as error:
            QMessageBox.warning(self, "Delete User Failed", str(error))
            return
        QMessageBox.information(self, "Delete User", f"Deleted user account: {deleted}")
        self.on_refresh()