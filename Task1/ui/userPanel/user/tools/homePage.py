from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
except ImportError:
    QWebEngineView = None
    
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.build_home_page()

    def build_home_page(self) -> QWidget:
        self.home_page = QFrame()
        self.home_page.setObjectName("card")
        self.home_layout = QVBoxLayout(self.home_page)
        self.init_home_title()
        self.init_stats_labels()
        self.init_home_data_table()
        self.init_warning_label()
        self.home_layout.addWidget(self.warning_label)
        self.home_layout.addStretch()
        # Add inner frame to this QWidget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.home_page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        return self.home_page

    def init_home_title(self) -> None:
        self.home_title = QLabel("User Dashboard")
        self.home_title.setObjectName("dashboardTitle")
        self.home_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.home_layout.addWidget(self.home_title)

    def init_stats_labels(self) -> None:
        self.stats_label = QLabel("Loading stats...")
        self.stats_label.setObjectName("statsLabel")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.home_layout.addWidget(self.stats_label)

    def init_home_data_table(self) -> None:     # Chart view similar to admin Daily Trend
        if QWebEngineView is not None:
            self.chart_view = QWebEngineView()
            self.chart_view.setMinimumHeight(320)
            self.chart_view.setMinimumWidth(640)
            self.chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.home_layout.addWidget(self.chart_view)
            self.chart_notice_label = QLabel("")
        else:
            self.chart_view = None
            self.chart_notice_label = QLabel(
                "Chart requires PySide6 WebEngine. Install it to view your borrowing chart."
            )
            self.chart_notice_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.home_layout.addWidget(self.chart_notice_label)
    
    def init_warning_label(self) -> None:
        self.warning_label = QLabel()
        self.warning_label.setObjectName("dashboardSummary")
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning_label.setStyleSheet("color:#b91c1c;font-weight:700;")
        self.home_layout.addWidget(self.warning_label)