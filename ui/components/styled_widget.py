from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

class StyledWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
