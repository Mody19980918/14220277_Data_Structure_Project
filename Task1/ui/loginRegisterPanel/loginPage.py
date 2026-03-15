from typing import Callable

from PySide6.QtWidgets import (
    QLineEdit,
    QMessageBox,
    QPushButton,
    QHBoxLayout, QWidget
)
from ui.loginRegisterPanel.loginRegisterBase import LoginRegisterBase

from models.user import User
from service.authService import AuthError, AuthService

class LoginPage(LoginRegisterBase):
    def __init__(
        self,
        auth_service: AuthService,
        open_register: Callable[[], None],
        on_login_success: Callable[[User], None],
    ) -> None:
        """
        Initialize the login page
        """
        super().__init__("Library Login")
        self.auth_service = auth_service
        self.open_register = open_register
        self.on_login_success = on_login_success
        self.init_username_input()
        self.init_password_input()
        self.init_login_button()
        self.init_register_button()
        self.init_buttons_container()

    def login_user(self) -> None:
        """
        Login a user with username and password
        """
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
        """
        Initialize the username input
        """
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.returnPressed.connect(self.login_user)
        self.card_layout.addWidget(self.username_input)

    def init_password_input(self):
        """
        Initialize the password input
        """
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.returnPressed.connect(self.login_user)
        self.card_layout.addWidget(self.password_input)

    def init_login_button(self):
        """
        Initialize the login button
        """
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_user)

    def init_register_button(self):
        """
        Initialize the register button
        """
        self.register_button = QPushButton("Register")
        self.register_button.setProperty("variant", "ghost")
        self.register_button.clicked.connect(self.open_register)

    def init_buttons_container(self):
        """
        Initialize the buttons container
        """
        self.btn_container = QWidget()
        self.btn_layout = QHBoxLayout(self.btn_container)
        self.btn_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_layout.addWidget(self.login_button )
        self.btn_layout.addWidget(self.register_button)
        self.card_layout.addWidget(self.btn_container)

