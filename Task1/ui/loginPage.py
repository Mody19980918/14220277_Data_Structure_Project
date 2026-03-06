from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLineEdit,
    QMessageBox,
    QPushButton,
    QHBoxLayout, QWidget
)
from ui.loginRegisterBase import LoginRegisterBase

from models.user import User
from service.authService import AuthError, AuthService


class LoginPage(LoginRegisterBase):
    def __init__(
        self,
        auth_service: AuthService,
        open_register: Callable[[], None],
        on_login_success: Callable[[User], None],
    ) -> None:
        super().__init__("Library Login")
        self.auth_service = auth_service
        self.open_register = open_register
        self.on_login_success = on_login_success
        self.init_username_input()
        self.init_password_input()
        self.init_login_button()
        self.init_register_button()
        self.init_buttons_container()

    def _login(self) -> None:
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            user = self.auth_service.login(username, password)
        except AuthError as error:
            QMessageBox.warning(self, "Login Failed", str(error))
            return

        self.password_input.clear()
        self.on_login_success(user)

    def init_username_input(self):
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.returnPressed.connect(self._login)
        self.card_layout.addWidget(self.username_input)

    def init_password_input(self):
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.returnPressed.connect(self._login)
        self.card_layout.addWidget(self.password_input)

    def init_login_button(self):
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self._login)

    def init_register_button(self):
        self.register_button = QPushButton("Register")
        self.register_button.setProperty("variant", "ghost")
        self.register_button.clicked.connect(self.open_register)

    def init_buttons_container(self):
        self.btn_container = QWidget()
        self.btn_layout = QHBoxLayout(self.btn_container)
        self.btn_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_layout.addWidget(self.login_button )
        self.btn_layout.addWidget(self.register_button)
        self.card_layout.addWidget(self.btn_container)

