import sys
import os
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from zen_explorer_core import repository
from explorer_ui.components import main as main_comp # , sidebar

def main():
    app = QApplication(sys.argv)
    # app.setStyleSheet(load_css("ui/explorer_themes/default"))
    repository.update_repository()
    repo = repository.data
    window = main_comp.MainWindow(repo)
    window.prepare()
    window.show()
    sys.exit(app.exec())

def load_css(directory):
    with open(f"{directory}/style.css", "r") as f:
        _style = f.read()
        if os.path.isfile(f"{directory}/variables.txt"):
            with open(f"{directory}/variables.txt", "r") as f2:
                _variables = f2.read()
                for line in _variables.splitlines():
                    try:
                        line = line.replace(' ', '')
                        var = line.split(':')[0].strip()
                        val = line.split(':')[1].strip()
                        _style = _style.replace(f"{var}", val)
                    except Exception as e:
                        pass
        return _style
