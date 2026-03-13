from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
except ImportError:
    QWebEngineView = None
from ui.userPanel.admin.tools.abstractPage import AbstractPage

class HomePage(AbstractPage):
    def __init__(self) -> None:
        super().__init__()
        self.init_home_page()
        self.init_home_layout()
        self.init_home_title()
        self.build_ui()

    def init_home_page(self) -> None:
        self.home_page = QFrame()
        self.home_page.setObjectName("card")
        # Set up main layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.home_page)

    def init_home_layout(self) -> None:
        self.home_layout = QVBoxLayout(self.home_page)
        self.home_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def init_home_title(self) -> None:
        self.home_title = QLabel("Daily Trend")
        self.home_title.setObjectName("title")
        self.home_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.home_layout.addWidget(self.home_title)

    def build_ui(self) -> None:
        if QWebEngineView is not None:
            self.chart_view = QWebEngineView()
            # Make the chart larger and allow it to expand to avoid cramped/mixed labels
            self.chart_view.setMinimumHeight(420)
            self.chart_view.setMinimumWidth(860)
            self.chart_view.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.home_layout.addWidget(self.chart_view)
            self.chart_notice_label = QLabel("")
        else:
            self.chart_view = None
            self.chart_notice_label = QLabel(
                "Chart requires PySide6 WebEngine. Install it to view plotly chart."
            )
            self.chart_notice_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.home_layout.addWidget(self.chart_notice_label)
        return self.home_page