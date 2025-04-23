import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout
)
from PySide6.QtCore import QEvent
from PySide6.QtGui import Qt
from explorer_ui.utils import images
from explorer_ui.components import theme_box as theme_box_component
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from explorer_ui.components.main import MainWindow
else:
    MainWindow = Any

class ThemeBrowseScreen(QWidget):
    def __init__(self, root: MainWindow, max_col=3):
        super().__init__()
        self._root: MainWindow = root
        self.repo = self._root.repository
        self.app = QApplication.instance()
        self.max_col = max_col
        self.grid = QGridLayout()
        self.grid_min_gap = 10
        self.grid.setHorizontalSpacing(self.grid_min_gap)
        self.grid.setVerticalSpacing(self.grid_min_gap)
        self.setLayout(self.grid)
        self.theme_boxes = []
        self.load_themes()
        self.previous_max_col = 0
        self.previous_row = 0
        self.resize(self._root.width())

    def load_themes(self):
        thumbnail = images.get_pixmap('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png') # placeholder for now
        print(f"{self.repo.themes}")
        for index, (theme_id, theme_data) in enumerate(self.repo.themes.items()):
            print(f"Loading theme {theme_id} with index {index}")
            theme_box = theme_box_component.ThemeBox(self.repo.get_theme(theme_id), thumbnail)
            theme_box.clicked.connect(lambda checked=False, theme=theme_data: self.load_theme(theme))
            self.grid.addWidget(theme_box, index // self.max_col, index % self.max_col)
            self.theme_boxes.append(theme_box)

    def load_theme(self, theme):
        # Get the widget at index 1 which is the ThemeScreen instance
        pass

    def resize(self, width):
        remaining = width - 20 - self.grid_min_gap
        max_col = 0
        while remaining >= 300 + self.grid_min_gap:
            remaining -= 300 + self.grid_min_gap
            max_col += 1

        if max_col == 0:
            return

        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        for col in range(self.previous_max_col):
            self.grid.setColumnMinimumWidth(col, 0)

        for row in range(self.grid.rowCount()):
            self.grid.setRowMinimumHeight(row, 0)
            self.grid.setRowStretch(row, 0)

        self.previous_max_col = max_col

        for col in range(max_col):
            self.grid.setColumnMinimumWidth(col, 300)
            self.grid.setColumnStretch(col, 0)

        row = 0
        col = 0

        for index, theme_box in enumerate(self.theme_boxes):
            if col >= max_col:
                col = 0
                row += 1
            self.grid.addWidget(theme_box, row, col)
            self.grid.setRowMinimumHeight(row, 223)
            self.grid.setRowStretch(row, 0)
            col += 1

        self.grid.setVerticalSpacing(10)

        self.previous_row = row

        self.setMinimumWidth(width - 20)
        self.setMaximumWidth(width - 20)
        self.setMinimumHeight(((row + 1) * 223) + (row * self.grid_min_gap))
        self.setMaximumHeight(((row + 1) * 223) + (row * self.grid_min_gap))
        self.setSizePolicy(self.sizePolicy().Policy.Fixed, self.sizePolicy().Policy.Fixed)

    def resizeEvent(self, event):
        self.resize(self._root.width())
