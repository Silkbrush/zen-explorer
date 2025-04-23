from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout
)
from explorer_ui.utils import images
from explorer_ui.components import theme_box as theme_box_component
from typing import TYPE_CHECKING, Any
import threading

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
        print(f"{self.repo.themes}")

        def get_thumbnail(theme,url):
            try:
                self._root.thumbnails[theme] = images.get_pixmap(url)
            except:
                pass

        threads = []
        for index, (theme_id, theme_data) in enumerate(self.repo.themes.items()):
            if theme_data.thumbnail and not theme_id in self._root.thumbnails.keys():
                thread = threading.Thread(target=get_thumbnail, args=(theme_id, theme_data.thumbnail))
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

        for index, (theme_id, theme_data) in enumerate(self.repo.themes.items()):
            print(f"Loading theme {theme_id} with index {index}")
            thumbnail = self._root.thumbnails.get(theme_id, self._root.default_thumbnail)
            theme_box = theme_box_component.ThemeBox(self._root, self.repo.get_theme(theme_id), thumbnail)
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
        max_heights = []

        for index, theme_box in enumerate(self.theme_boxes):
            if col >= max_col:
                col = 0
                row += 1
            self.grid.addWidget(theme_box, row, col)
            self.grid.setRowMinimumHeight(row, theme_box.height())
            self.grid.setRowStretch(row, 1)
            col += 1

            if len(max_heights) <= row:
                max_heights.append(theme_box.height())
            else:
                max_heights[row] = max(max_heights[row], theme_box.height())

        self.grid.setVerticalSpacing(10)

        self.previous_row = row

        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
        self.setMinimumHeight(sum(max_heights) + (row * self.grid_min_gap))
        self.setMaximumHeight(sum(max_heights) + (row * self.grid_min_gap))
        self.adjustSize()
        self.setSizePolicy(self.sizePolicy().Policy.Fixed, self.sizePolicy().Policy.Fixed)

    def resizeEvent(self, event):
        self.resize(self.parentWidget().width())
