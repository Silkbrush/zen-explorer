from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QSizePolicy
)
from PySide6.QtGui import Qt, QPixmap
from explorer_ui.models import pages
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from explorer_ui.components.main import MainWindow
else:
    MainWindow = Any

class ThemeBox(QWidget):
    clicked = Signal()  # Define the signal at class level for PySide6

    def __init__(self, root: MainWindow, theme_data, thumbnail):
        super().__init__()
        self._root = root

        # Enable mouse tracking to handle mouse events
        self.setMouseTracking(True)

        self.theme_data = theme_data
        self.thumbnail = QPixmap(thumbnail)
        self.thumbnail_label = QLabel()
        # self.thumbnail_label.setPixmap(self.thumbnail)

        aspect_ratio = thumbnail.width() / thumbnail.height()
        new_height = int(280 / aspect_ratio)

        self.thumbnail_label.setPixmap(thumbnail.scaled(
            300,
            new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.thumbnail_label.setMinimumHeight(new_height)

        # Prepare layout
        layout = QVBoxLayout()
        layout.addWidget(self.thumbnail_label)
        self.setLayout(layout)

        # Set theme name
        self.theme_name = QLabel(theme_data.name)
        self.theme_name.setWordWrap(True)
        self.theme_name.adjustSize()
        self.theme_name.setObjectName("themeName")
        layout.addWidget(self.theme_name, alignment=Qt.AlignmentFlag.AlignTop)

        # Set theme author
        self.theme_author = QLabel('By ' + theme_data.author)
        self.theme_author.setWordWrap(True)
        self.theme_author.adjustSize()
        self.theme_author.setObjectName("themeAuthor")
        layout.addWidget(self.theme_author, alignment=Qt.AlignmentFlag.AlignTop)

        # Set theme description (max 100 chars)
        self.theme_description = QLabel(theme_data.description[:97] + '...' if len(theme_data.description) > 100 else theme_data.description)
        self.theme_description.adjustSize()
        self.theme_description.setWordWrap(True)
        self.theme_description.adjustSize()
        self.theme_description.setMinimumHeight(48)
        self.theme_description.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.theme_description.setObjectName("themeDescription")
        layout.addWidget(self.theme_description, alignment=Qt.AlignmentFlag.AlignTop)

        # Set dimensions
        self.setMinimumWidth(300)
        self.setMaximumWidth(300)
        self.setMinimumHeight(new_height + 128)
        self.setMaximumHeight(new_height + 128)

        # Do not expand/shrink the widget horizontally, but allow vertical expansion
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        # Make the widget look clickable with cursor change
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Optional: add some visual feedback with style
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            ThemeBox {
                border-radius: 4px;
                padding: 5px;
            }
            
            ThemeBox:hover {
                background-color: rgba(200, 200, 200, 0.3);
            }
            
            ThemeBox QLabel {
                color: white;
                background-color: transparent;
                margin: 0px;
                padding: 0px;
                line-height: 100%;
            }
            
            ThemeBox #themeName {
                font-size: 14px;
                font-weight: bold;
            }
        """)

        # Show theme on click
        self.clicked.connect(lambda: self._show_theme())

    def mousePressEvent(self, event):
        # Emit clicked signal when the widget is clicked
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def _show_theme(self):
        self._root.theme = self._root.repository.get_theme(self.theme_data.id)
        self._root.navigate(pages.Pages.overview)
