from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QWidget,
    QLabel,
)
from zen_explorer_core.repository import RepositoryData
from .theme_screen import ThemeScreen
from .theme_browse_screen import ThemeBrowseScreen
from .components.top_bar import TopBar

class NavUI(QWidget):
    def __init__(self, repo: RepositoryData):
        super().__init__()

        layout = QHBoxLayout()

        self.screens = QStackedWidget()
        self.screens.addWidget(ThemeScreen(self))
        self.screens.addWidget(ThemeBrowseScreen(self, repo))
        layout.addWidget(self.screens)

        self.topbar = TopBar(self)
        self.topbar.setObjectName("TopBar")
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.topbar)
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(top_bar_layout)
        main_layout.addLayout(layout)
        self.switch_screen(1)
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
    def get_current_screen(self):
        return self.screens.currentWidget()

    def switch_screen(self, index):
        self.screens.setCurrentIndex(index)
        if index == 0:
            self.topbar.install_btn.show()
        else:
            self.topbar.install_btn.hide()