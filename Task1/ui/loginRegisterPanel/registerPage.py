from typing import Callable

from PySide6.QtWidgets import QLineEdit, QMessageBox, QPushButton, QHBoxLayout, QWidget
from ui.loginRegisterPanel.loginRegisterBase import LoginRegisterBase

from service.authService import AuthService
from service.authError import AuthError


class RegisterPage(LoginRegisterBase):
    def __init__(self, auth_service: AuthService, back_to_login: Callable[[], None]) -> None:
        """
        Initialize the register page
        """
        super().__init__("Create Account")
        self.auth_service = auth_service
        self.back_to_login = back_to_login
        self.init_username_input()
        self.init_password_input()
        self.init_button_layout()
        self.init_register_button()
        self.init_login_button()

    def register_user(self) -> None:
        """
        Register a user with username and password
        """
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            self.auth_service.register_user(username, password)
        except AuthError as error:
            QMessageBox.warning(self, "Register Failed", str(error))
            return

        self.username_input.clear()
        self.password_input.clear()
        QMessageBox.information(self, "Register", "Account created successfully.")
        self.back_to_login()

    def init_username_input(self):
        """
        Initialize the username input
        """
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.card_layout.addWidget(self.username_input)

    def init_password_input(self):
        """
        Initialize the password input
        """
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password (at least 8 chars)")
        self.card_layout.addWidget(self.password_input)

    def init_button_layout(self):
        """
        Initialize the button layout
        """
        self.btn_container = QWidget()
        self.btn_layout = QHBoxLayout(self.btn_container)
        self.card_layout.addWidget(self.btn_container)

    def init_register_button(self):
        """
        Initialize the register button
        """
        self.btn_layout.setContentsMargins(0, 0, 0, 0)
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)
        self.btn_layout.addWidget(self.register_button)
    
    def init_login_button(self):
        """
        Initialize the login button
        """
        self.login_button = QPushButton("Back Login")
        self.login_button.setProperty("variant", "ghost")
        self.login_button.clicked.connect(self.back_to_login)
        self.btn_layout.addWidget(self.login_button)



