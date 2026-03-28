from PySide6.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

class CommonFunction:

    def confirm_action(self, parent: QWidget, title: str, message: str) -> bool:
        """
        Confirm the action.
        Include parent, title and message.
        """
        dialog = QMessageBox(parent)
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setWindowTitle(title)
        dialog.setText(message)
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
        return dialog.clickedButton() == yes_button

    def centered_action_button_cell(self, button: QPushButton) -> QWidget:
        """
        Centered the action button cell.
        Include button.
        """
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button)
        return container
