import sys
from PySide6.QtWidgets import (
    QApplication,
)
from zen_explorer_core.repository import update_repository
from zen_explorer_core import repository
from .main_window import MainWindow
from .util import load_css

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_css("ui/explorer_themes/default"))
    update_repository()
    repo = repository.data
    
    window = MainWindow(repo)
    window.show()
    app.setStyle
    sys.exit(app.exec())