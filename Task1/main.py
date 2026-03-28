import sys

from PySide6.QtWidgets import QApplication

from ui.homePage import HomePage
from ui.pageStyle import APP_STYLE


def main() -> int:
    """
    Main function to run the application.
    """
    page = QApplication(sys.argv)
    page.setStyleSheet(APP_STYLE)
    window = HomePage()
    window.show()
    return page.exec()

if __name__ == "__main__":
    main()
