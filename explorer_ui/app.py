import sys
import os
from PySide6.QtWidgets import QApplication
from zen_explorer_core import repository
from explorer_ui.components import main as main_comp # , sidebar

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_css("explorer_ui/explorer_themes/default"))
    repository.update_repository()
    repo = repository.data
    window = main_comp.MainWindow(repo)
    window.prepare()
    window.show()
    sys.exit(app.exec())

def load_css(directory):
    file = f"{directory}/style.css" if os.path.isfile(f"{directory}/style.css") else f"{directory}/style.qss"
    with open(file, "r") as f:
        _style = f.read()
        if os.path.isfile(f"{directory}/variables.txt"):
            with open(f"{directory}/variables.txt", "r") as f2:
                _variables = f2.read()
                for line in _variables.splitlines():
                    try:
                        line = line.replace(' ', '')
                        line = line.replace(';', '') # Some users might like semicolons at the end of lines.
                        var = line.split(':')[0].strip()
                        val = line.split(':')[1].strip()
                        _style = _style.replace(f"{var}", val)
                    except Exception:
                        pass
        return _style
