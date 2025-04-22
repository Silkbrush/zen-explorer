import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
)
from PySide6.QtGui import Qt
from zen_explorer_core.repository import RepositoryData

from .util import get_pixmap_from_url
from .components.theme_box import ThemeBox

class ThemeBrowseScreen(QWidget):
    def __init__(self, navui, repo: RepositoryData, max_col=3):
        super().__init__()
        self.repo = repo
        self.app = QApplication.instance()
        self.navui = navui
        self.max_col = max_col
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.theme_boxes = []
        self.load_themes()
        self.resize_themes()
        self.resize_allowed_time = time.time()

    def load_themes(self):
        thumbnail = get_pixmap_from_url('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png') # placeholder for now
        print(f"{self.repo.themes}")
        for index, (theme_id, theme_data) in enumerate(self.repo.themes.items()):
            print(f"Loading theme {theme_id} with index {index}")
            theme_box = ThemeBox(self.repo.get_theme(theme_id), thumbnail)
            theme_box.clicked.connect(lambda checked=False, theme=theme_data: self.load_theme(theme))
            self.grid.addWidget(theme_box, index // self.max_col, index % self.max_col)
            self.theme_boxes.append(theme_box)

    def load_theme(self, theme):
        # Get the widget at index 1 which is the ThemeScreen instance
        self.navui.switch_screen(1)
        theme_screen = self.navui.screens.widget(1)
        theme_screen.load_theme(theme)
        print(theme_screen)

    def resize_themes(self):
        for theme_box in self.theme_boxes:
            original_thumbnail = theme_box.thumbnail

            new_width = self.width()/self.max_col - 10

            if original_thumbnail.width() > 0 and original_thumbnail.height() > 0:
                aspect_ratio = original_thumbnail.width() / original_thumbnail.height()
                new_height = int(new_width / aspect_ratio)

                scaled_pixmap = original_thumbnail.scaled(
                    new_width,
                    new_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                theme_box.thumbnail_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        if time.time() > self.resize_allowed_time:
            print("Resizing themes")
            self.resize_themes()
            self.resize_allowed_time = time.time() + 0.4