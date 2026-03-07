from functools import partial

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QStyle,
)

from models.book import Book
from models.loan import Loan
from service.authError import BorrowError, ReturnError
from service.userPanelService import UserPanelService
from ui.userPanel.user.tools.borrowPage import BorrowPage
from ui.userPanel.user.tools.returnPage import ReturnPage
from ui.userPanel.user.tools.homePage import HomePage


class UserPanel(QWidget):
    def __init__(
        self, username: str, user_service: UserPanelService, on_logout
    ) -> None:
        super().__init__()
        self.username = username
        self.user_service = user_service
        self.on_logout = on_logout
        self.home_page = HomePage()
        self.borrow_page = BorrowPage(on_category_changed=self.refresh_available_books)
        self.return_page = ReturnPage()
        self.build_ui()
        self.refresh_all()

    def build_ui(self) -> None:
        self.init_layout()
        self.init_nav_card()
        self.init_hello_label()
        self.init_menu_entries()
        self.init_logout_button()
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
        self.hello_label = QLabel(f"Hello, {self.username}")
        self.hello_label.setObjectName("greeting")
        self.hello_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nav_layout.addWidget(self.hello_label)

    def init_menu_entries(self) -> None:
        menu_entries = [
            ("Home", 0, QStyle.StandardPixmap.SP_DirHomeIcon),
            ("Borrow", 1, QStyle.StandardPixmap.SP_FileDialogNewFolder),
            ("Return", 2, QStyle.StandardPixmap.SP_ArrowBack),
        ]
        for label, index, icon_type in menu_entries:
            self.button = QPushButton(label)
            self.button.setProperty("variant", "ghost")
            self.button.setProperty("nav", "true")
            self.button.setIcon(self.style().standardIcon(icon_type))
            self.button.setIconSize(QSize(16, 16))
            self.button.clicked.connect(partial(self.switch_page, index))
            self.nav_layout.addWidget(self.button)

    def init_logout_button(self) -> None:
        self.logout_button = QPushButton("Logout")
        self.logout_button.setProperty("nav", "true")
        self.logout_button.clicked.connect(self.on_logout)
        self.nav_layout.addWidget(self.logout_button)

    def init_pages(self) -> None:
        self.pages = QStackedWidget()
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.borrow_page)
        self.pages.addWidget(self.return_page)

    def switch_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        if index == 1:
            self.refresh_categories()
        elif index == 2:
            self.refresh_borrowed_books()
        else:
            self.refresh_home_summary()

    def refresh_all(self) -> None:
        self.refresh_home_summary()
        self.refresh_categories()
        self.refresh_borrowed_books()

    def refresh_home_summary(self) -> None:
        summary = self.user_service.home_summary(self.username)
        # Update stats label
        stats_text = (
            f"<b>Borrowed:</b> {summary['borrowed_count']} books | "
            f"<b>This Month:</b> {summary['borrowed_this_month']} | "
            f"<b>This Week:</b> {summary['borrowed_this_week']}"
        )
        if summary["expired_count"] > 0:
            stats_text += f" | <b style='color:red;'>Expired: {summary['expired_count']}</b>"
        self.home_page.stats_label.setText(stats_text)
        self.home_page.warning_label.setText(
            "Warning: You have expired books." if summary["has_expired"] else ""
        )
        # populate chart HTML if available
        chart_html = self.user_service.daily_user_chart_html(self.username)
        if self.home_page.chart_view is not None and chart_html:
            self.home_page.chart_view.setHtml(chart_html)
            self.home_page.chart_notice_label.setText("")
        elif self.home_page.chart_view is not None:
            self.home_page.chart_view.setHtml(
                "<h3 style='text-align:center;'>No borrowing data yet.</h3>"
            )
            self.home_page.chart_notice_label.setText("")
        elif chart_html is None:
            self.home_page.chart_notice_label.setText(
                "No borrowing data or pandas/plotly is not installed."
            )

    def refresh_categories(self) -> None:
        categories = self.user_service.list_categories()
        self.borrow_page.category_combo.blockSignals(True)
        self.borrow_page.category_combo.clear()
        self.borrow_page.category_combo.addItems(categories)
        self.borrow_page.category_combo.blockSignals(False)
        if categories:
            self.refresh_available_books(categories[0])
        else:
            self.borrow_table.setRowCount(0)

    def refresh_available_books(self, category: str) -> None:
        books = self.user_service.list_available_books(category)
        self.borrow_page.borrow_table.setRowCount(len(books))
        for row, book in enumerate(books):
            self.fill_borrow_row(row, book)

    def fill_borrow_row(self, row: int, book: Book) -> None:
        self.init_borrow_row_category_item(row, book)
        self.init_borrow_row_book_item(row, book)
        self.init_borrow_row_button(row, book)
    
    def init_borrow_row_category_item(self, row: int, book: Book) -> QTableWidgetItem:
        category_item = QTableWidgetItem(book.category)
        category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.borrow_page.borrow_table.setItem(row, 0, category_item)

    def init_borrow_row_book_item(self, row: int, book: Book) -> QTableWidgetItem:
        book_item = QTableWidgetItem(book.name)
        book_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.borrow_page.borrow_table.setItem(row, 1, book_item)

    def init_borrow_row_button(self, row: int, book: Book) -> QPushButton:
        button = QPushButton("Borrow")
        button.setProperty("size", "small")
        button.clicked.connect(partial(self.borrow_book, book.name))
        self.borrow_page.borrow_table.setCellWidget(row, 2, self.centered_button_cell(button))

    def borrow_book(self, book_name: str) -> None:
        try:
            self.user_service.borrow_book(self.username, book_name)
        except BorrowError as error:
            QMessageBox.warning(self, "Borrow Failed", str(error))
            return
        self.show_centered_info("Borrow", f"You borrowed {book_name}.")
        self.refresh_all()

    def refresh_borrowed_books(self) -> None:
        loans = self.user_service.list_borrowed_books(self.username)
        self.return_page.return_table.setRowCount(len(loans))
        for row, loan in enumerate(loans):
            self.fill_return_row(row, loan)

    def fill_return_row(self, row: int, loan: Loan) -> None:
        self.init_due_item(row, loan)
        self.init_book_item(row, loan)
        self.init_return_button(row, loan)
    
    def init_due_item(self,row:int, loan: Loan) -> QTableWidgetItem:
        due_item = QTableWidgetItem(loan.due_date)
        due_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_page.return_table.setItem(row, 0, due_item)

    def init_book_item(self,row:int, loan: Loan) -> QTableWidgetItem:
        book_item = QTableWidgetItem(loan.book_name)
        book_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_page.return_table.setItem(row, 1, book_item)

    def init_return_button(self,row:int, loan: Loan) -> QPushButton:
        button = QPushButton("Return")
        button.setProperty("size", "small")
        button.clicked.connect(partial(self.return_book, loan.book_name))
        self.return_page.return_table.setCellWidget(row, 2, self.centered_button_cell(button))

    def centered_button_cell(self, button: QPushButton) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button)
        return container

    def return_book(self, book_name: str) -> None:
        try:
            self.user_service.return_book(self.username, book_name)
        except ReturnError as error:
            QMessageBox.warning(self, "Return Failed", str(error))
            return
        self.show_centered_info("Return", f"You returned {book_name}.")
        self.refresh_all()

    def show_centered_info(self, title: str, message: str) -> None:
        self.init_message_box(title, message)
        self.init_message_text_label()

        self.message_box.exec()

    def init_message_box(self, title: str, message: str) -> None:
        self.message_box = QMessageBox(self)
        self.message_box.setIcon(QMessageBox.Icon.Information)
        self.message_box.setWindowTitle(title)
        self.message_box.setText(message)
        self.message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

    def init_message_text_label(self) -> None:
        self.text_label = self.message_box.findChild(QLabel, "qt_msgbox_label")
        if self.text_label is not None:
            self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.text_label.setMinimumWidth(260)

    def init_message_layout(self) -> None:
        self.layout = self.message_box.layout()
        if self.layout is not None:
            self.layout.setSpacing(6)
            self.layout.setContentsMargins(10, 10, 10, 10)
