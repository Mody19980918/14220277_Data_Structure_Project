from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)
from PySide6.QtCore import Qt
from ui.userPanel.admin.tools.abstractPage import AbstractPage

class AddBookPage(AbstractPage):
    def __init__(self, on_refresh) -> None:
        super().__init__()
        self.on_refresh = on_refresh
        self.init_add_book_page()
        self.init_add_book_layout()
        self.init_add_book_title()
        self.init_add_category_select()
        self.init_add_book_name_input()
        self.init_add_quantity_input()
        self.init_add_book_form()
        self.init_add_book_button()
        self.init_add_book_page_layout()

    def init_add_book_page(self) -> None:
        self.add_book_page = QFrame()
        self.add_book_page.setObjectName("card")
        # Set up main layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.add_book_page)

    def init_add_book_layout(self) -> None:
        self.add_book_layout = QVBoxLayout(self.add_book_page)
        self.add_book_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

    def init_add_book_title(self) -> None:
        self.add_book_title = QLabel("Add Book")
        self.add_book_title.setObjectName("title")
        self.add_book_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_book_layout.addWidget(self.add_book_title)

    def init_add_book_form(self) -> None:
        # Make Add Book layout mirror User Home: stacked, centered content
        self.form_vbox = QVBoxLayout()
        self.form_vbox.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        self.form_vbox.addWidget(self.category_label)
        self.form_vbox.addWidget(self.add_category_select)
        self.form_vbox.addSpacing(8)
        self.form_vbox.addWidget(self.book_name_label)
        self.form_vbox.addWidget(self.add_book_name_input)
        self.form_vbox.addSpacing(8)
        self.form_vbox.addWidget(self.quantity_label)
        self.form_vbox.addWidget(self.add_quantity_input)

        self.form_container = QWidget()
        self.form_container.setLayout(self.form_vbox)
        self.form_container.setMaximumWidth(520)
        self.add_book_layout.addWidget(self.form_container)

    def init_add_category_select(self) -> None:
        self.category_label = QLabel("Category")
        self.category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_category_select = QComboBox()
        self.add_category_select.setMaximumWidth(360)

    def init_add_book_name_input(self) -> None:
        self.book_name_label = QLabel("Book Name")
        self.book_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_book_name_input = QLineEdit()
        self.add_book_name_input.setPlaceholderText("Book name")
        self.add_book_name_input.setMaximumWidth(360)

    def init_add_quantity_input(self) -> None:
        self.quantity_label = QLabel("Quantity")
        self.quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_quantity_input = QLineEdit()
        self.add_quantity_input.setPlaceholderText("Quantity")
        self.add_quantity_input.setMaximumWidth(360)

    def init_add_book_button(self) -> None:
        self.add_book_button = QPushButton("Add / Increase Book")
        self.add_book_button.setMaximumWidth(240)
        self.add_book_button.clicked.connect(self.add_book)
        self.btn_row = QHBoxLayout()
        self.btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_row.addWidget(self.add_book_button)
        self.add_book_layout.addLayout(self.btn_row)

    def init_add_book_page_layout(self) -> None:
        self.add_book_layout.addLayout(self.btn_row)
        self.add_book_layout.addStretch(1)

    def add_book(self) -> None:
        category = self.add_category_select.currentText().strip()
        book_name = self.add_book_name_input.text().strip()
        quantity_text = self.add_quantity_input.text().strip()
        try:
            quantity = int(quantity_text)
            created = self.admin_service.add_book(category, book_name, quantity)
        except ValueError as error:
            QMessageBox.warning(self, "Add Book Failed", str(error))
            return

        QMessageBox.information(
            self,
            "Add Book",
            f"Book updated: {created.name} ({created.category}) x {created.quantity}",
        )
        self.add_book_name_input.clear()
        self.add_quantity_input.clear()
        self.on_refresh()