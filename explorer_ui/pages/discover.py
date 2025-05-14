from typing_extensions import Optional
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QGridLayout
)

from explorer_ui.models.widgets import QWidget
from explorer_ui.components.sidebar import SideBar
from explorer_ui.utils import images
from explorer_ui.components import theme_box as theme_box_component
from typing import TYPE_CHECKING, Any
import threading
from thefuzz import fuzz

from zen_explorer_core.models.theme import ThemeType

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
        self._layout = QHBoxLayout()
        self.grid = QGridLayout()
        self.sidebar = SideBar(self)
        self._layout.addWidget(self.sidebar)
        self._layout.addLayout(self.grid)
        self.grid_min_gap = 10
        self.grid.setHorizontalSpacing(self.grid_min_gap)
        self.grid.setVerticalSpacing(self.grid_min_gap)
        self.setLayout(self._layout)
        self.previous_max_col = 0
        self.previous_row = 0
        self.theme_boxes = []
        self.active_tags = []
        self.active_types = []
        self.load_themes()
        self.resize(self._root.width())

    def _remove_themes(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            print('removed ', widget)
            if widget is not None:
                widget.deleteLater()

    def load_themes(self, themes: Optional[dict]=None):
        self._remove_themes()
        self.theme_boxes = []
        themes = themes if themes else self.repo.themes
        print(f"loading themes {themes}")
        def get_thumbnail(theme,url):
            try:
                self._root.thumbnails[theme] = images.get_pixmap(url)
            except:
                pass

        threads = []
        for index, (theme_id, theme_data) in enumerate(themes.items()):
            if theme_data.thumbnail and theme_id not in self._root.thumbnails.keys():
                thread = threading.Thread(target=get_thumbnail, args=(theme_id, theme_data.thumbnail))
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

        for index, (theme_id, theme_data) in enumerate(themes.items()):
            thumbnail = self._root.thumbnails.get(theme_id, self._root.default_thumbnail)
            theme_box = theme_box_component.ThemeBox(self._root, self.repo.get_theme(theme_id), thumbnail)
            theme_box.clicked.connect(lambda checked=False, tid=theme_id: self.load_theme(self.repo.get_theme(tid)))
            # self.grid.addWidget(theme_box, index // self.max_col, index % self.max_col)
            self.theme_boxes.append(theme_box)

        self.update()
        self.resize(self.width())

    def search(self, query):
        def get_sort_key(item, query):
            key, obj = item
            # Compute the fuzzy ratio based on the `name` attribute 
            return fuzz.ratio(obj.name, query)

        filtered_items = filter(lambda x: get_sort_key(x, query) > 30, self.repo.themes.items())
        sorted_items = sorted(filtered_items, key=lambda item: get_sort_key(item, query), reverse=True)
        sorted_dict = dict(sorted_items)
        self.load_themes(sorted_dict)
        print([(obj.name, get_sort_key((key, obj), query)) for key, obj in self.repo.themes.items()])

    def collapse_sidebar(self):
        self.sidebar.hide()

    def filter_by_tag(self, tag: str, active: bool):
        return 
        # if active and tag not in self.active_tags:
        #     self.active_tags.append(tag)  
        # elif tag in self.active_tags and not active: 
        #     self.active_tags.remove(tag)
        # 
        # def filter_tags(item):
        #     key, obj = item
        #     if len(self.active_tags) == 0:
        #         return True
        #     else:
        #         for tag in self.active_tags:
        #             if tag in obj.tags:
        #                 return True
        #         return False
        #     
        # 
        # filtered_items = filter(lambda x: filter_tags(x), self.repo.themes.items())

    def filter_by_type(self, type: ThemeType, active: bool):
        if active and type not in self.active_types:
            self.active_types.append(type)
        elif type in self.active_types and not active:
            self.active_types.remove(type)

        def filter_types(item):
            key, obj = item
            if len(self.active_types) == 0:
                return True
            else:
                for active_type in self.active_types:
                    if obj.type == active_type:
                        return True
                return False

        filtered_items = filter(lambda x: filter_types(x), self.repo.themes.items())
        self.load_themes(dict(filtered_items))
        

    def load_theme(self, theme):
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
            row = index // max_col
            col = index % max_col
            self.grid.addWidget(theme_box, row, col)

            if len(max_heights) <= row:
                max_heights.append(theme_box.height())
            else:
                max_heights[row] = max(max_heights[row], theme_box.height())

            self.grid.setRowMinimumHeight(row, theme_box.height())
            self.grid.setRowStretch(row, 1)

        self.grid.setVerticalSpacing(10)
        self.previous_row = (len(self.theme_boxes) - 1) // max_col

        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
        self.setMinimumHeight(sum(max_heights) + (row * self.grid_min_gap))
        self.setMaximumHeight(sum(max_heights) + (row * self.grid_min_gap))
        self.adjustSize()
        self.setSizePolicy(self.sizePolicy().Policy.Fixed, self.sizePolicy().Policy.Fixed)

    def resizeEvent(self, event):
        self.resize(self.parentWidget().width())

