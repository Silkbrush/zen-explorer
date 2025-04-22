from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PySide6.QtGui import Qt, QPixmap
from .styled_widget import StyledWidget

class ThemeBox(StyledWidget):
    clicked = Signal()  # Define the signal at class level for PySide6

    def __init__(self, theme_data, thumbnail):
        super().__init__()

        # Enable mouse tracking to handle mouse events
        self.setMouseTracking(True)

        self.theme_data = theme_data
        self.thumbnail = QPixmap(thumbnail)
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setPixmap(self.thumbnail)
        layout = QVBoxLayout()
        layout.addWidget(self.thumbnail_label)
        self.label = QLabel(theme_data.name)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # Make the widget look clickable with cursor change
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Optional: add some visual feedback with style
        self.setStyleSheet("""
            Theme_Box {
                border-radius: 8px;
                padding: 5px;
            }
            Theme_Box:hover {
                background-color: rgba(200, 200, 200, 0.3);
            }
        """)

    def mousePressEvent(self, event):
        # Emit clicked signal when the widget is clicked
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)