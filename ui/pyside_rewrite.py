import sys
import time
from typing_extensions import Never
from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QWidget,
    QLabel,
    QGridLayout,
    QComboBox,
    QScrollArea,
)
from zen_explorer_core import installer
from zen_explorer_core.models.theme import Theme
import requests
import os
from PySide6.QtGui import Qt, QPixmap, QTextDocument
from zen_explorer_core.repository import RepositoryData
from zen_explorer_core.profiles import get_profile_path, get_profiles
from zen_explorer_core.repository import update_repository
from zen_explorer_core import repository
from github import Github
import re
import markdown

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

        # Set the widget for the scroll area
        self.scrollable_area.setWidget(scroll_content)

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

        # Add the README content display
        readme_heading = QLabel("README")
        readme_heading.setStyleSheet("font-size: 14pt; font-weight: bold; margin-top: 20px;")
        self.main_box.addWidget(readme_heading)

        self.main_box.addWidget(self.get_readme_item())

        # Add stretch to push everything to the top
        self.main_box.addStretch()

    def get_readme(self):
        try:
            pattern = r"^https?://github\.com/([^/]+/[^/]+)"
            match = re.search(pattern, self.homepage)
            return self.github.get_repo(match.group(1)).get_readme().decoded_content.decode('utf-8')
        except Exception as e:
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
            theme_box = Theme_Box(self.repo.get_theme(theme_id), thumbnail)
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

class Theme_Box(QWidget):
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

def get_pixmap_from_url(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        image_data = response.content
        pixmap = QPixmap()
        if pixmap.loadFromData(image_data):
            return pixmap
        else:
            print("Failed to load image from data.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image: {e}")

class NavUI(QWidget):
    def __init__(self, repo: RepositoryData):
        super().__init__()

        layout = QHBoxLayout()

        self.screens = QStackedWidget()
        self.screens.addWidget(ThemeBrowseScreen(self, repo))
        self.screens.addWidget(ThemeScreen(self))
        layout.addWidget(self.screens)

        self.topbar = TopBar(self)
        bottom_bar_layout = QHBoxLayout()
        bottom_bar_layout.addWidget(QLabel("Bottom Bar"))
        bottom_bar_layout.addStretch()

        # Wrap central layout and bottom bar in a vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.topbar)
        main_layout.addLayout(layout)


        self.setLayout(main_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
    def get_current_screen(self):
        return self.screens.currentWidget()

    def switch_screen(self, index):
        self.screens.setCurrentIndex(index)
        if index == 1:
            self.topbar.install_btn.show()
        else:
            self.topbar.install_btn.hide()

class TopBar(QWidget):
    def __init__(self, navui):
        super().__init__()
        self.setObjectName("TopBar")
        self.setProperty("type", "navigation")
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.navui = navui

        self.screens = [
            'discover',
            'options',
            'tweaks',
            'manage'
        ]
        self.navigator_layout = QHBoxLayout()
        self.main_layout.addLayout(self.navigator_layout)

        self.main_layout.addStretch()

        self.profile_layout = QHBoxLayout()
        self.main_layout.addLayout(self.profile_layout)

        self.create_navigation()
        profile_switcher = self.create_profile_switcher()
        self.install_btn = QPushButton('Install')
        self.profile_layout.addWidget(self.install_btn)
        self.install_btn.clicked.connect(lambda _: self.install(self.display_profile_to_profile[self.option_combo_box.currentText()]))
        self.install_btn.hide()
        self.profile_layout.addWidget(profile_switcher)
        
        
    def install(self, profile_id):
        print('Installing...')
        try:
            self.navui.get_current_screen().install_theme(profile_id)
        except Exception as e:
            print(f'Error installing: {e}')

    def toggle_install_btn_visibility(self, val: bool|None = None):
        if val is None:
            new_visibility = not self.install_btn.isVisible()
        else:
            new_visibility = val
        print(f'setting visibility to {new_visibility}')

        if new_visibility:
            print('Button shown')
            self.install_btn.show()
        else:
            print('Button hidden')
            self.install_btn.hide()


    def create_navigation(self):
        for i, screen in enumerate(self.screens):
            button = QPushButton(screen.capitalize())
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    color: #555555;
                }
                QPushButton:pressed {
                    color: #e58e27;
                }
            """)
            self.navigator_layout.addWidget(button)
            print(f'Button {i} created')
            button.clicked.connect(lambda _, i=i: self.show_screen(index=i))

    def create_profile_switcher(self):
        self.profiles_display = []
        self.profiles = []
        self.display_profile_to_profile = {}
        print(get_profiles())

        for profile in get_profiles():
            profile_id, profile_name = profile.split('.', 1)
            display_text = f'{profile_name} ({profile_id})'
            self.profiles_display.append(display_text)
            self.profiles.append(profile)
            print(profile)
            print(get_profile_path(profile))
            self.display_profile_to_profile[display_text] = profile

        # Create QComboBox instance for profile selection
        self.option_combo_box = QComboBox()
        self.option_combo_box.addItems(self.profiles_display)
        self.option_combo_box.setPlaceholderText("Select profile")

        # Connect the selection change signal to the slot
        self.option_combo_box.currentIndexChanged.connect(self.user_select)

        # Layout management
        
        self.option_combo_box.setGeometry(self.width() - 200, 10, 150, 30)  # Adjust geometry as needed
        return self.option_combo_box

    def user_select(self, profile):
        print(f"Selected profile: {profile}")

    def show_screen(self, index):
        print(f"Showing screen {index}")
        self.navui.switch_screen(index)

class MainWindow(QMainWindow):
    def __init__(self, repo: RepositoryData):
        super().__init__()
        self.resize(800, 600)
        # Set the window title
        self.setWindowTitle("Silkthemes")

        self.navui = NavUI(repo)

        self.setCentralWidget(self.navui)

def main():
    app = QApplication(sys.argv)
    # app.setStyleSheet(load_css("ui/explorer_themes/default"))
    update_repository()
    repo = repository.data
    window = MainWindow(repo)
    window.show()
    window.setStyleSheet('background-color: #01000000;')

    sys.exit(app.exec())

def load_css(directory):
    with open(f"{directory}/style.css", "r") as f:
        _style = f.read()
        if os.path.isfile(f"{directory}/variables.txt"):
            with open(f"{directory}/variables.txt", "r") as f:
                _variables = f.read()
                for line in _variables.splitlines():
                    line = line.replace(' ', '')
                    var = line.split(':')[0].strip()
                    val = line.split(':')[1].strip()
                    _style = _style.replace(f"{var}", val)
        return _style

if __name__ == "__main__":
    main()
