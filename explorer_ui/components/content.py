from PySide6.QtWidgets import QScrollArea, QWidget
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from explorer_ui.components.main import MainWindow
else:
    MainWindow = Any

class Content(QScrollArea):
    def __init__(self, root: MainWindow):
        super().__init__()
        self._root: MainWindow = root
        self.setObjectName("content")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('border: none;')
        self.setMinimumHeight(500)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Internal variables
        self.__ready: bool = False
        self.__widget: Optional[QWidget] = None

    def set_content(self, widget):
        """Set the content of the scroll area."""
        self.setWidget(widget)
        self.__widget = widget

    # Prepare method
    def prepare(self):
        """Prepares the widget for use."""

        # Do not run if already prepared
        if self.__ready:
            raise RuntimeError('widget is already prepared')

        # Set ready state
        self.__ready = True

    def resizeEvent(self, event):
        """Resize event for the widget."""
        super().resizeEvent(event)
        if self.__widget:
            self.__widget.resizeEvent(event)

