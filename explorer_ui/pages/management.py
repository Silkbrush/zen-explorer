from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from ui.components import theme_box
from ui.main_window import MainWindow
from zen_explorer_core import installer, profiles, repository
import time

class ThemeManagementScreen(QWidget):
    def __init__(self, root: MainWindow):
        super().__init__(root)
        self._root = root
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(10, 10, 10, 10)
        self.update_themes()
        self.setLayout(self._layout)
        self.allowresizeon = time.time()
        
    def update_themes(self):
        profile = f'{self._root.profile.id}.{self._root.profile.name}'
        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:  # If it's a layout, clear it recursively
                child_layout = item.layout()
                if child_layout is not None:
                    while child_layout.count() > 0:
                        child_item = child_layout.takeAt(0)
                        child_widget = child_item.widget()
                        if child_widget is not None:
                            child_widget.deleteLater()
        for theme in profiles.get_installed(profile):
            print(theme)
            buttonwidget = QWidget()
            main_button_layout = QHBoxLayout(buttonwidget)
            main_button_layout.setContentsMargins(10, 10, 10, 10)
            theme_data = repository.data.get_theme(theme)
            theme_button = QCheckBox(theme_data.name)
            theme_button.setCheckable(True)
            # theme_button.setStyleSheet('background-color: #222; border-radius: 10px; padding: 8px;')
            buttonwidget.setLayout(main_button_layout)
            main_button_layout.addWidget(theme_button)
            main_button_layout.addStretch()
            self._layout.addWidget(buttonwidget)

            action_button_layout = QHBoxLayout()
            main_button_layout.addLayout(action_button_layout)
            
            if installer.is_installed(profile, theme):
                button = QPushButton('uninstall')
                button.clicked.connect(lambda theme=theme, profile=profile: self._uninstall(theme, profile))
                action_button_layout.addWidget(button)
                button.setStyleSheet("""
                    QPushButton {
                        border: none;
                        padding: 5px;
                        margin-left: 10px;
                        border-radius: 4px;
                        color: red;
                    }
                    QPushButton:hover {
                        color: #333;
                    }
                """)
            buttonwidget.setStyleSheet("""
                QWidget {
                    background-color: #222;
                    border-radius: 10px;
                    padding: 8px;
                }
            """)
    def resize(self, width):
        self.setMinimumWidth(width)
        
    def resizeEvent(self, event):
        if time.time() > self.allowresizeon:
            print("Resizing...")
            self.update_themes()
            self.allowresizeon = time.time() + 0.3
        super().resizeEvent(event)
        
        
    def _uninstall(self, theme, profile):
        try:
            print(f"Uninstalling theme {theme} in {profile}...")
            installer.uninstall_theme(profile, theme, staging=True)
            print('staging passed')
            installer.uninstall_theme(profile, theme)
            print('uninstall completed')
        except Exception as e:
            print(f"Error uninstalling theme {theme}: {e}")
        self.update_themes()

