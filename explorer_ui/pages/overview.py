from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
    QScrollArea,
)
from zen_explorer_core import installer
from PySide6.QtGui import Qt
from zen_explorer_core import repository
import re
import markdown
from explorer_ui.utils import images
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from explorer_ui.components.main import MainWindow
else:
    MainWindow = Any

class ThemeScreen(QWidget):
    def __init__(self, root: MainWindow):
        super().__init__()
        self._root = root
        self.theme = root.theme
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        if not root.theme:
            raise ValueError('theme is not set')

        self.thumbnail = images.get_pixmap(
            'https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png'
        )

        # Create widgets
        self.wrapper = QVBoxLayout()
        self.info_area = QWidget()
        self.readme_area = QWidget()
        self.wrapper.addWidget(self.info_area)
        self.wrapper.addWidget(self.readme_area)
        self.scrollable_area = QScrollArea()
        self.scrollable_area.setWidgetResizable(True)

        # Set layout
        self.setLayout(self.wrapper)

        # Create header area with name and author side by side
        header_layout = QHBoxLayout()
        name_label = QLabel(self.theme.name)
        name_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: white;")
        author_label = QLabel(f"by {self.theme.author}")
        author_label.setStyleSheet("font-size: 12pt; color: #ccc;")

        header_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignBottom)
        header_layout.addWidget(author_label, alignment=Qt.AlignmentFlag.AlignBottom)
        header_layout.addStretch()
        self.wrapper.addLayout(header_layout)

        # Add description below header
        description_label = QLabel(self.theme.description)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 11pt; margin: 10px 0; color: white;")
        self.wrapper.addWidget(description_label)

        # Add a separator line
        separator = QWidget()
        separator.setFixedHeight(1)
        self.wrapper.addWidget(separator)

        # Create thumbnail wrapper so we can horizontally center it
        thumbnail_wrapper = QHBoxLayout()
        thumbnail_wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wrapper.addLayout(thumbnail_wrapper)

        # Add thumbnail below description
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setStyleSheet(
            "margin: 20px; padding: 10px; background-color: #f5f5f5; border-radius: 8px;")
        new_width = 500
        aspect_ratio = self.thumbnail.width() / self.thumbnail.height()
        new_height = int(new_width / aspect_ratio)
        self.thumbnail_label.setPixmap(
            self.thumbnail.scaled(
                new_width,
                new_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        self.thumbnail_label.setMinimumHeight(new_height)
        self.thumbnail_label.setMaximumHeight(new_height)
        thumbnail_wrapper.addWidget(self.thumbnail_label)

        separator = QWidget()
        separator.setFixedHeight(1)
        self.wrapper.addWidget(separator)

        self.wrapper.addWidget(self.get_readme_item())

        # Add stretch to push everything to the top
        self.wrapper.addStretch()

        print(f'Theme {self.theme.id} loaded')

    def install_theme(self, profile_id):
        if not repository.data or not repository.data.themes:
            print('No themes available.')
            return

        print(f'Installing {self.theme.id} by {self.theme.author}...')
        try:
            installer.install_theme(profile_id, self.theme.id)
        except:
            print('Failed to install theme.')
            raise
        print('Theme installed.')

    def get_readme(self):
        return self._root.repository.get_theme_readme(self.theme.id) or 'No README available'

    def get_readme_item(self):
        # Get the markdown text
        markdown_text = self.get_readme()

        # Convert markdown to HTML without image processing
        html_content = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])

        # Strip out image tags to prevent loading issues
        html_content = re.sub(r'<img[^>]*>', '', html_content)

        # Create a simple QLabel to display the HTML
        text_label = QLabel()
        text_label.setTextFormat(Qt.TextFormat.RichText)
        text_label.setOpenExternalLinks(True)
        text_label.setWordWrap(True)

        # Set stylesheet for better readability
        text_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                color: white;
            }
        """)

        # Set the HTML content directly
        text_label.setText(html_content)

        return text_label

    def resize_event(self, event):
        self.resize(self.parentWidget().width())
        super().resizeEvent(event)

    def resize(self, width):
        self.setMinimumWidth(width)
