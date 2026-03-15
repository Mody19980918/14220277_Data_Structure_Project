from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QStyle, QVBoxLayout, QWidget


class LoginRegisterBase(QWidget):

    def __init__(self, title: str) -> None:
        """
        Initialize the login register base for login and register page to inherit
        """
        super().__init__()
        self.build_common_ui(title)

    def build_common_ui(self, title: str) -> None:
        """
        Build the common UI for login and register page
        """
        self.init_card()
        self.init_root()
        self.init_icon()
        self.init_title(title)

    def init_root(self):
        """
        Initialize the root layout
        """
        root_layout = QVBoxLayout(self)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.addWidget(self.card, 1, Qt.AlignmentFlag.AlignCenter)
        self.root_layout = root_layout
        
    def init_title(self, title: str):
        title_label = QLabel(title)
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_layout.addWidget(title_label)

    def init_card(self):
        """
        Initialize the card
        """
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(740)
        card.setMaximumWidth(920)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(30, 28, 30, 28)
        self.card = card
        self.card_layout = card_layout

    def init_icon(self):
        """
        Initialize the icon
        """
        icon_row = QHBoxLayout()
        icon_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for icon_type in (
            QStyle.StandardPixmap.SP_DirHomeIcon,
            QStyle.StandardPixmap.SP_FileDialogInfoView,
            QStyle.StandardPixmap.SP_DialogApplyButton,
        ):
            icon_label = QLabel()
            icon_label.setPixmap(self.style().standardIcon(icon_type).pixmap(22, 22))
            icon_row.addWidget(icon_label)
        self.card_layout.addLayout(icon_row)

