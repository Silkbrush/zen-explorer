from PySide6.QtWidgets import (
    QMainWindow,
)
from zen_explorer_core.repository import RepositoryData
from .nav_ui import NavUI

class MainWindow(QMainWindow):
    def __init__(self, repo: RepositoryData):
        super().__init__()
        self.resize(800, 600)
        # Set the window title
        self.setWindowTitle("Silkthemes")

        self.navui = NavUI(repo)

        self.setCentralWidget(self.navui)