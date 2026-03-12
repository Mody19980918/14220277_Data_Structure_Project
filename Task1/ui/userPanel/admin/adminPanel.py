from functools import partial

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QFrame,
    QStyle,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from service.adminPanelService import AdminPanelService
from ui.userPanel.admin.tools.homePage import HomePage
from ui.userPanel.admin.tools.payPage import PayPage
from ui.userPanel.admin.tools.addBookPage import AddBookPage
from ui.userPanel.admin.tools.addCategoryPage import AddCategoryPage
from ui.userPanel.admin.tools.deleteBookPage import DeleteBookPage
from ui.userPanel.admin.tools.deleteCategoryPage import DeleteCategoryPage
from ui.userPanel.admin.tools.deleteUserPage import DeleteUserPage
from ui.userPanel.admin.commonFunction import CommonFunction

class AdminPanel(QWidget):
    def __init__(self, username: str, admin_service: AdminPanelService, on_logout) -> None:
        super().__init__()
        self.username = username
        self.admin_service = admin_service
        self.on_logout = on_logout
        self.common_function = CommonFunction()
        self.menu = [
            ("Daily Trend", 0, QStyle.StandardPixmap.SP_DirHomeIcon),
            ("Pay", 1, QStyle.StandardPixmap.SP_DialogApplyButton),
            ("Add Book", 2, QStyle.StandardPixmap.SP_FileDialogNewFolder),
            ("Add Category", 3, QStyle.StandardPixmap.SP_FileDialogListView),
            ("Delete Book", 4, QStyle.StandardPixmap.SP_TrashIcon),
            ("Delete Category", 5, QStyle.StandardPixmap.SP_TrashIcon),
            ("Delete User", 6, QStyle.StandardPixmap.SP_ComputerIcon),
        ]

        self.home_page = HomePage()
        self.pay_page = PayPage(on_refresh=self.refresh_daily_trend)
        self.add_book_page = AddBookPage(on_refresh=self.refresh_delete_book_categories)
        self.add_category_page = AddCategoryPage( on_refresh=self.refresh_categories)
        self.delete_book_page = DeleteBookPage(
            on_refresh_categories=self.refresh_categories,
            on_refresh_delete_book_categories=self.refresh_delete_book_categories,
            on_refresh_books_for_category=self.refresh_delete_books_for_category
        )
        self.delete_category_page = DeleteCategoryPage( on_refresh=self.refresh_categories)
        self.delete_user_page = DeleteUserPage( on_refresh=self.reset_delete_user_search)

        self.build_ui()
        self.refresh_all()

    def build_ui(self) -> None:
        self.init_layout()
        self.init_nav_card()
        self.init_hello_label()
        self.init_buttons()
        self.init_pages()
        self.layout.addWidget(self.nav_card, 1)
        self.layout.addWidget(self.pages, 4)

    def init_layout(self) -> None:
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(12)
    
    def init_nav_card(self) -> None:
        self.nav_card = QFrame()
        self.nav_card.setObjectName("card")
        self.nav_layout = QVBoxLayout(self.nav_card)
        self.nav_layout.setSpacing(12)
        self.nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    def init_hello_label(self) -> None:
        self.hello_label = QLabel(f"Admin, {self.username}")
        self.hello_label.setObjectName("greeting")
        self.hello_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nav_layout.addWidget(self.hello_label)
    
    def init_buttons(self) -> None:
        for text, index, icon_type in self.menu:
            button = QPushButton(text)
            button.setProperty("variant", "ghost")
            button.setProperty("nav", "true")
            button.setIcon(self.style().standardIcon(icon_type))
            button.setIconSize(QSize(16, 16))
            button.clicked.connect(partial(self.switch_page, index))
            self.nav_layout.addWidget(button)
        
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setProperty("nav", "true")
        self.logout_btn.clicked.connect(self.on_logout)
        self.nav_layout.addWidget(self.logout_btn)

    def init_pages(self) -> None:
        self.pages = QStackedWidget()
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.pay_page)
        self.pages.addWidget(self.add_book_page)
        self.pages.addWidget(self.add_category_page)
        self.pages.addWidget(self.delete_book_page)
        self.pages.addWidget(self.delete_category_page)
        self.pages.addWidget(self.delete_user_page)

    def switch_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        if index == 0:
            self.refresh_daily_trend()
        if index in {2, 5}:
            self.refresh_categories()
        if index == 4:
            self.refresh_delete_book_categories()
        if index == 6:
            self.reset_delete_user_search()

    def refresh_all(self) -> None:
        self.refresh_daily_trend()
        self.refresh_categories()
        self.refresh_delete_book_categories()
        self.refresh_delete_categories_table()
        self.reset_delete_user_search()
        self.pay_page.confirm_paid_button.setVisible(False)
        self.pay_page.pay_result_table.setVisible(False)
        self.pay_page.fine_result_label.setText("No result yet.")

    def refresh_daily_trend(self) -> None:
        chart_html = self.admin_service.daily_trend_chart()
        chart_view = getattr(self.home_page, 'chart_view', None)
        chart_notice_label = getattr(self.home_page, 'chart_notice_label', None)

        if chart_view is not None and chart_html:
            chart_view.setHtml(chart_html)
            if chart_notice_label:
                chart_notice_label.setText("")
        elif chart_view is not None:
            chart_view.setHtml("<h3 style='text-align:center;'>No trend data yet.</h3>")
            if chart_notice_label:
                chart_notice_label.setText("")
        elif chart_html is None and chart_notice_label:
            chart_notice_label.setText(
                "No trend data yet or pandas/plotly is not installed."
            )

    def refresh_categories(self) -> None:
        categories = self.admin_service.list_categories()
        self.add_book_page.add_category_select.clear()
        self.add_book_page.add_category_select.addItems(categories)
        self.refresh_delete_categories_table()

    def refresh_delete_book_categories(self) -> None:
        categories = self.admin_service.list_categories()
        self.delete_book_page.delete_book_category_select.blockSignals(True)
        self.delete_book_page.delete_book_category_select.clear()
        self.delete_book_page.delete_book_category_select.addItems(categories)
        self.delete_book_page.delete_book_category_select.blockSignals(False)
        if categories:
            self.refresh_delete_books_for_category(categories[0])
        else:
            self.delete_book_page.delete_book_table.setRowCount(0)

    def refresh_delete_books_for_category(self, category: str) -> None:
        books = self.admin_service.list_books_by_category(category)
        self.delete_book_page.delete_book_table.setRowCount(len(books))
        for row, book in enumerate(books):
            book_item = QTableWidgetItem(book.name)
            book_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.delete_book_page.delete_book_table.setItem(row, 0, book_item)
            delete_button = QPushButton("Delete")
            delete_button.setProperty("size", "small")
            delete_button.clicked.connect(partial(self.delete_book_page.delete_book, book.name))
            self.delete_book_page.delete_book_table.setCellWidget(
                row, 1, self.common_function.centered_action_button_cell(delete_button)
            )

    def refresh_delete_categories_table(self) -> None:
        categories = self.admin_service.list_categories()
        self.delete_category_page.delete_category_table.setRowCount(len(categories))
        for row, category in enumerate(categories):
            category_item = QTableWidgetItem(category)
            category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.delete_category_page.delete_category_table.setItem(row, 0, category_item)
            delete_button = QPushButton("Delete")
            delete_button.setProperty("size", "small")
            delete_button.clicked.connect(partial(self.delete_category_page.delete_category, category))
            self.delete_category_page.delete_category_table.setCellWidget(
                row, 1, self.common_function.centered_action_button_cell(delete_button)
            )

    def reset_delete_user_search(self) -> None:
        self.delete_user_page.delete_user_result_label.setText("No result yet.")
        self.delete_user_page.delete_user_table.setVisible(False)
        self.delete_user_page.delete_user_button.setVisible(False)



