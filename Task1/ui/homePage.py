from PySide6.QtWidgets import QMainWindow, QStackedWidget
from ui.loginRegisterPanel.loginPage import LoginPage
from ui.loginRegisterPanel.registerPage import RegisterPage
from service.authService import AuthService
from service.userPanelService import UserPanelService
from service.adminPanelService import AdminPanelService
from models.user import User
from ui.userPanel.user.userPanel import UserPanel
from ui.userPanel.admin.adminPanel import AdminPanel

class HomePage(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.resize(980, 640)
        self.user_panel: UserPanel | None = None
        self.admin_panel: AdminPanel | None = None
        self.init_service()
        self.init_page()
        self.init_stack()
        self.show_login()

    def init_service(self):
        self.auth_service = AuthService()
        self.user_service = UserPanelService()
        self.admin_service = AdminPanelService()

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
        if user.role == "admin":
            self.show_admin_panel(user.username)
            return
        if self.user_panel is not None:
            self.stack.removeWidget(self.user_panel)
            self.user_panel.deleteLater()
        self.user_panel = UserPanel(
            username=user.username,
            user_service=self.user_service,
            on_logout=self.show_login,
        )
        self.stack.addWidget(self.user_panel)
        self.stack.setCurrentWidget(self.user_panel)

    def show_admin_panel(self, username: str) -> None:
        if self.admin_panel is not None:
            self.stack.removeWidget(self.admin_panel)
            self.admin_panel.deleteLater()
        self.admin_panel = AdminPanel(
            username=username,
            admin_service=self.admin_service,
            on_logout=self.show_login,
        )
        self.stack.addWidget(self.admin_panel)
        self.stack.setCurrentWidget(self.admin_panel)




