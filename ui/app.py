import sys
from PySide6.QtWidgets import (
    QApplication,
)
from zen_explorer_core.repository import update_repository
from zen_explorer_core import repository
from .main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    # app.setStyleSheet(load_css("ui/explorer_themes/default"))
    update_repository()
    repo = repository.data
    window = MainWindow(repo)
    window.show()
    window.setStyleSheet('background-color: #01000000;')

    sys.exit(app.exec())