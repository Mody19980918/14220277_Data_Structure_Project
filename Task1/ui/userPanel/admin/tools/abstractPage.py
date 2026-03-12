from abc import ABCMeta
from PySide6.QtWidgets import QWidget
from service.adminPanelService import AdminPanelService
from ui.userPanel.admin.commonFunction import CommonFunction

# Create a metaclass that combines ABCMeta and QWidget's metaclass
class AbstractPageMeta(ABCMeta, type(QWidget)):
    pass

class AbstractPage(QWidget, metaclass=AbstractPageMeta):
    def __init__(self):
        super().__init__()
        self.admin_service = AdminPanelService()
        self.common_function = CommonFunction()
