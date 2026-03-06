from PySide6.QtWidgets import QMainWindow, QStackedWidget
from ui.loginRegisterPanel.loginPage import LoginPage
from ui.loginRegisterPanel.registerPage import RegisterPage
from service.authService import AuthService
from models.user import User

class HomePage(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.resize(980, 640)
        self.init_service()
        self.init_page()
        self.init_stack()
        self.show_login()
    
    def init_service(self):
        self.auth_service = AuthService()

    def init_page(self):
        self.login_page = LoginPage(
            auth_service=self.auth_service,
            open_register=self.show_register,
            on_login_success=self.show_user_panel,
        )
        self.register_page = RegisterPage(
            auth_service=self.auth_service,
            back_to_login=self.show_login,
        )

    def init_stack(self):
        self.stack = QStackedWidget()
        self.stack.setObjectName("appRoot")
        self.setCentralWidget(self.stack)

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
    def show_login(self) -> None:
        self.stack.setCurrentWidget(self.login_page)

    def show_register(self) -> None:
        self.stack.setCurrentWidget(self.register_page)

    def show_user_panel(self, user: User) -> None:
        return 



