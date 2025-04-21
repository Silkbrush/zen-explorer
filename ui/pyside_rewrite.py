import sys
import time
from PySide6.QtCore import QSize
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
    QComboBox
)
import requests
import os
from PySide6.QtGui import Qt, QPixmap
from zen_explorer_core.repository import RepositoryData
from zen_explorer_core.profiles import get_profile_path, get_profiles

class Theme_select(QWidget):
    def __init__(self, stacked_widget, repo: RepositoryData, max_col=3):
        super().__init__()
        self.repo = repo
        self.stacked_widget = stacked_widget
        self.max_col = max_col
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.theme_boxes = []
        self.load_themes()
        self.resize_themes()
        self.resize_allowed_time = time.time()

    def load_themes(self):
        thumbnail = get_pixmap_from_url('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png') # placeholder for now
        for index, theme in enumerate(self.repo.themes):
            print(f"Loading theme {theme} with index {index}")
            theme_box = Theme_Box(self.repo.get_theme(theme), thumbnail)
            self.grid.addWidget(theme_box, index // self.max_col, index % self.max_col)
            self.theme_boxes.append(theme_box)
            
    def resize_themes(self):
        for theme_box in self.theme_boxes:
            scaled_pixmap = theme_box.thumbnail.scaled(self.width()/self.max_col - 10, 
                self.height()/self.max_col - 10, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            theme_box.thumbnail_label.setPixmap(scaled_pixmap)
            
    def resizeEvent(self, event):
        if time.time() > self.resize_allowed_time:
            print("Resizing themes")
            self.resize_themes()
            self.resize_allowed_time = time.time() + 0.1

class Theme_Box(QWidget):
    def __init__(self, theme_data, thumbnail):
        super().__init__()
        self.theme_data = theme_data
        self.thumbnail = QPixmap(thumbnail)
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setPixmap(self.thumbnail)
        layout = QVBoxLayout()
        layout.addWidget(self.thumbnail_label)
        self.label = QLabel(theme_data.name)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

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
        self.screens.addWidget(Theme_select(self.screens, repo))
        layout.addWidget(self.screens)

        # self.sidebar = QWidget()
        # sidebar_layout = QVBoxLayout()
        # self.sidebar.setLayout(sidebar_layout)
        # self.sidebar.setObjectName("Sidebar")
        # self.sidebar.setProperty("type", "navigation")

        # sidebar_layout.addWidget(QLabel("Sidebar"))
        # sidebar_layout.addWidget(QPushButton("Button 1"))
        # sidebar_layout.addWidget(QPushButton("Button 2"))
        # sidebar_layout.addStretch()
        # layout.addWidget(self.sidebar)

        self.topbar = TopBar(self.screens)
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

class TopBar(QWidget):
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.setObjectName("TopBar")
        self.setProperty("type", "navigation")
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.stacked_widget = stacked_widget
        
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
        self.create_profile_switcher()
        
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
        self.profile_layout.addWidget(self.option_combo_box)
        self.option_combo_box.setGeometry(self.width() - 200, 10, 150, 30)  # Adjust geometry as needed
        
    def user_select(self, profile):
        print(f"Selected profile: {profile}")
        
    def show_screen(self, index):
        print(f"Showing screen {index}")
        self.stacked_widget.setCurrentIndex(index)
    
class MainWindow(QMainWindow):
    def __init__(self, repo: RepositoryData):
        super().__init__()
        self.resize(800, 600)
        # Set the window title
        self.setWindowTitle("Silkthemes")

        nav_ui = NavUI(repo)

        self.setCentralWidget(nav_ui)

def main():
    from cli import repository
    repo = repository.data
    print(repo.themes)
    app = QApplication(sys.argv)
    # app.setStyleSheet(load_css("ui/explorer_themes/default"))
    window = MainWindow(repo)
    window.show()

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
