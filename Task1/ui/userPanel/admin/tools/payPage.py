from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
    QMessageBox,
    QAbstractItemView
)
from PySide6.QtCore import Qt

class PayPage(QWidget):
    def __init__(self, on_refresh=None) -> None:
        super().__init__()
        self.on_refresh = on_refresh
        self.init_pay_page()
        self.init_pay_title()
        self.init_pay_search_row()
        self.init_fine_result_label()
        self.init_pay_result_table()
        self.init_confirm_paid_button()

    def init_pay_page(self) -> None:
        self.pay_page = QFrame()
        self.pay_page.setObjectName("card")
        # Set up main layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.pay_page)

    def init_pay_title(self) -> None:
        self.pay_layout = QVBoxLayout(self.pay_page)
        self.pay_title = QLabel("Pay Fines")
        self.pay_title.setObjectName("title")
        self.pay_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pay_layout.addWidget(self.pay_title)

    def init_pay_search_row(self) -> None:
        self.search_row = QHBoxLayout()
        self.search_user_input = QLineEdit()
        self.search_user_input.setPlaceholderText("Search username")
        self.search_row.addWidget(self.search_user_input)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_fines)
        self.search_row.addWidget(self.search_button)
        self.pay_layout.addLayout(self.search_row)

    def init_fine_result_label(self) -> None:
        self.fine_result_label = QLabel("No result yet.")
        self.fine_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fine_result_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        self.pay_layout.addWidget(self.fine_result_label)

    def init_pay_result_table(self) -> None:
        self.pay_result_table = QTableWidget(1, 3)
        self.pay_result_table.setHorizontalHeaderLabels(["User", "Count", "Amount"])
        self.pay_result_table.verticalHeader().setVisible(False)
        self.pay_result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.pay_result_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.pay_result_table.setMaximumHeight(84)
        self.pay_result_table.setVisible(False)
        self.pay_result_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.pay_layout.addWidget(self.pay_result_table)
    
    def init_confirm_paid_button(self) -> None:
        self.confirm_paid_button = QPushButton("Confirm Paid")
        self.confirm_paid_button.clicked.connect(self.confirm_paid)
        self.confirm_paid_button.setVisible(False)
        self.pay_layout.addWidget(self.confirm_paid_button)
        self.pay_layout.addStretch(1)

    def search_fines(self) -> None:
        """Search for user fines based on username input"""
        username = self.search_user_input.text().strip()
        if not username:
            self.fine_result_label.setText("Please enter a username.")
            self.pay_result_table.setVisible(False)
            self.confirm_paid_button.setVisible(False)
            return

        result = self.admin_service.find_user_fines(username)
        if not result.get("found", False):
            self.fine_result_label.setText("User not found")
            self.pay_result_table.setVisible(False)
            self.confirm_paid_button.setVisible(False)
            return

        count = int(result["count"])
        amount = float(result["amount"])
        self.fine_result_label.setText("")
        self._set_pay_result_row(result["username"], str(count), f"{amount:.2f}")
        self.pay_result_table.setVisible(True)
        self.confirm_paid_button.setVisible(count > 0 and amount > 0)

    def set_pay_result_row(self, user: str, count: str, amount: str) -> None:
        user_item = QTableWidgetItem(user)
        count_item = QTableWidgetItem(count)
        amount_item = QTableWidgetItem(amount)
        for item in (user_item, count_item, amount_item):
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pay_result_table.setItem(0, 0, user_item)
        self.pay_result_table.setItem(0, 1, count_item)
        self.pay_result_table.setItem(0, 2, amount_item)

    def confirm_paid(self) -> None:
        """Confirm payment of fines"""
        username = self.search_user_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Pay", "Please input username first.")
            return

        result = self.admin_service.find_user_fines(username)
        if not result.get("found", False):
            self.fine_result_label.setText("User not found")
            self.pay_result_table.setVisible(False)
            self.confirm_paid_button.setVisible(False)
            QMessageBox.warning(self, "Pay", "User not found.")
            return

        # Confirm dialog
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setWindowTitle("Confirm Payment")
        dialog.setText(f"Confirm to process fine payment for user '{username}'?")
        yes_button = dialog.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        no_button = dialog.addButton("No", QMessageBox.ButtonRole.NoRole)
        yes_button.setStyleSheet(
            "background:#dc2626;color:white;border-radius:6px;padding:6px 14px;"
        )
        no_button.setStyleSheet(
            "background:#16a34a;color:white;border-radius:6px;padding:6px 14px;"
        )
        dialog.setDefaultButton(no_button)
        dialog.exec()

        if dialog.clickedButton() != yes_button:
            return

        updated = self.admin_service.mark_fines_as_paid(username)
        QMessageBox.information(self, "Pay", f"Marked {updated} fine records as paid.")

        # Refresh the search results
        self.search_fines()

        # Notify parent that payment is complete (for refreshing daily trend)
        self.on_refresh()