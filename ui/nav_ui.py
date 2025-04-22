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
        self.screens.addWidget(ThemeBrowseScreen(self, repo))
        self.screens.addWidget(ThemeScreen(self))
        layout.addWidget(self.screens)

        self.topbar = TopBar(self)
        bottom_bar_layout = QHBoxLayout()
        bottom_bar_layout.addWidget(QLabel("Bottom Bar"))
        bottom_bar_layout.addStretch()

        # Wrap central layout and bottom bar in a vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.topbar)
        main_layout.addLayout(layout)


        self.setLayout(main_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
    def get_current_screen(self):
        return self.screens.currentWidget()

    def switch_screen(self, index):
        self.screens.setCurrentIndex(index)
        if index == 1:
            self.topbar.install_btn.show()
        else:
            self.topbar.install_btn.hide()