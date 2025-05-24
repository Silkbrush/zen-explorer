from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
    QScrollArea,
)
from zen_explorer_core import installer
from zen_explorer_core.models.theme import Theme
from PySide6.QtGui import Qt
from PySide6.QtCore import Qt as QtCore
from zen_explorer_core import repository
from github import Github
import re
import markdown
from .util import get_pixmap_from_url

class ThemeScreen(QWidget):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

    def load_theme(self, theme: Theme):
        self.id = theme.id
        self.github = Github()
        self.name = theme.name
        self.author = theme.author
        self.description = theme.description
        self.homepage = theme.homepage
        self.thumbnail = get_pixmap_from_url('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png')  # in the future theme.thumbnail
        self.create_widgets()
        print(f'Theme loaded: {self.name}')
        
    def install_theme(self, profile_id):
        if not repository.data or not repository.data.themes:
            print('No themes available.')
            return
            
        print(f'Installing {self.id} by {self.author}...')
        try:
            installer.install_theme(profile_id, self.id)
        except:
            print('Failed to install theme.')
            raise
        print('Theme installed.')
        
    def create_widgets(self):
        self.main_box = QVBoxLayout()

        self.scrollable_area = QScrollArea()
        
        self.scrollable_area.setWidgetResizable(True)

        # Create a container widget to hold the layout
        scroll_content = QWidget()
        scroll_content.setLayout(self.main_box)
        scroll_content.setObjectName('ThemeScrollArea')

        
        # Set the widget for the scroll area
        self.scrollable_area.setWidget(scroll_content)
        self.scrollable_area.setVerticalScrollBarPolicy(QtCore.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollable_area.setHorizontalScrollBarPolicy(QtCore.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollable_area.setObjectName('ThemeScrollContainer')

        # Create a layout for this widget and add the scroll area to it
        layout = QVBoxLayout()
        layout.addWidget(self.scrollable_area)
        self.setLayout(layout)

        # Create header area with name and author side by side
        header_layout = QHBoxLayout()
        name_label = QLabel(self.name)
        name_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        author_label = QLabel(f"by {self.author}")
        author_label.setStyleSheet("font-size: 12pt; color: #555;")

        header_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignBottom)
        header_layout.addWidget(author_label, alignment=Qt.AlignmentFlag.AlignBottom)
        header_layout.addStretch()
        self.main_box.addLayout(header_layout)

        # Add description below header
        description_label = QLabel(self.description)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 11pt; margin: 10px 0;")
        self.main_box.addWidget(description_label)

        # Add a separator line
        separator = QWidget()
        separator.setFixedHeight(1)
        self.main_box.addWidget(separator)

        # Add thumbnail below description
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setStyleSheet("margin: 20px; padding: 10px; background-color: #f5f5f5; border-radius: 8px;")
        self.resize_thumbnail()
        self.main_box.addWidget(self.thumbnail_label)

        separator = QWidget()
        separator.setFixedHeight(1)
        self.main_box.addWidget(separator)
        
        self.main_box.addWidget(self.get_readme_item())

        # Add stretch to push everything to the top
        self.main_box.addStretch()

    def get_readme(self):
        try:
            pattern = r"^https?://github\.com/([^/]+/[^/]+)"
            match = re.search(pattern, self.homepage)
            return self.github.get_repo(match.group(1)).get_readme().decoded_content.decode('utf-8')
        except Exception:
            return 'No README available'

    def get_readme_item(self):
        from PySide6.QtWidgets import QLabel
        from PySide6.QtCore import Qt

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

        # Set a sensible maximum width
        text_label.setMaximumWidth(800)

        # Set stylesheet for better readability
        text_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                padding: 10px;
            }
        """)

        # Set the HTML content directly
        text_label.setText(html_content)

        return text_label

    def resize_event(self, event):
        self.resize_thumbnail()
        super().resizeEvent(event)

    def resize_thumbnail(self):
        self.thumbnail_label.setPixmap(self.thumbnail.scaled(int(self.width()/3), int(self.height()/3),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation))