from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget as QWidgetStandard

class QWidget(QWidgetStandard):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)