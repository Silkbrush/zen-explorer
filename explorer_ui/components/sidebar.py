from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QCheckBox

from explorer_ui.models.widgets import QWidget
from zen_explorer_core.models.theme import ThemeType


class SideBar(QWidget):
    def __init__(self, screen):
        super().__init__()
        self._screen = screen
        self._layout = QVBoxLayout(self)
        self.setStyleSheet('background-color: #222; margin: 10px; margin-bottom: 0; border: none; border-radius: 6px;')
        self.setLayout(self._layout)
        self.tags = {
            # 'test1': partial(self._screen.filter_by_tag, 'test1'),
            # 'test2': partial(self._screen.filter_by_tag, 'test2'),
        }
        self.types = {
            'bundles': partial(self._screen.filter_by_type, ThemeType.bundle),
            'themes': partial(self._screen.filter_by_type, ThemeType.chrome),
            'pages': partial(self._screen.filter_by_type, ThemeType.content),
        }
        self.create_widgets()

    def create_widgets(self):
        if len(self.types) > 0:
            label = QLabel('Type')
            label.setStyleSheet("font-weight: bold;")
            self._layout.addWidget(label)

        for type, action in self.types.items():
            checkbox = QCheckBox(type)
            checkbox.stateChanged.connect(lambda state, a=action: a(state))
            self._layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignTop)

        if len(self.tags) > 0:
            label = QLabel('Tags')
            label.setStyleSheet("font-weight: bold;")
            self._layout.addWidget(label)

        for tag, action in self.tags.items():
            checkbox = QCheckBox(tag)
            checkbox.stateChanged.connect(lambda state, a=action: a(state))
            self._layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignTop)

        self._layout.addStretch()
