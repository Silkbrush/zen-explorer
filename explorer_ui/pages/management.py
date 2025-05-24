import time
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from zen_explorer_core import installer, profiles, repository
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from explorer_ui.components.main import MainWindow
else:
    MainWindow = Any

class ThemeManagementScreen(QWidget):
    def __init__(self, root: MainWindow):
        super().__init__(root)
        self._root = root
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(10, 10, 10, 10)
        self.update_themes()
        self.setLayout(self._layout)
        self.allowresizeon = time.time()

    # noinspection PyUnresolvedReferences,PyUnboundLocalVariable
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
            # theme_button = QCheckBox(theme_data.name)
            # theme_button.toggled.connect(lambda: self._button_toggle())
            # theme_button.setCheckable(True)
            theme_button = QPushButton(theme_data.name)

            buttonwidget.setLayout(main_button_layout)
            main_button_layout.addWidget(theme_button)
            main_button_layout.addStretch()
            self._layout.addWidget(buttonwidget)

            action_button_layout = QHBoxLayout()
            main_button_layout.addLayout(action_button_layout)

            # Uninstall Button
            uninstall_button = QPushButton('Uninstall')
            uninstall_button.clicked.connect(
                lambda _, theme=theme, profile=profile: self._uninstall(theme, profile)
            )
            uninstall_button.setStyleSheet("""
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
            action_button_layout.addWidget(self._create_update_button(profile, theme))
            action_button_layout.addWidget(self._create_enable_button(profile, theme))
            action_button_layout.addWidget(uninstall_button)

    # def _button_toggle(self):
    #     pass
    
    def _create_update_button(self, profile, theme):
        is_updateable = installer.is_updateable(profile, theme)
        button_data = {
            'text': 'Update' if is_updateable else 'Up to date',
            'action': (lambda _=None, t=theme, p=profile:
                       self._update(t, p)),
            'objectName': 'updateButton' if is_updateable else 'uptodateLabel',
        }
        update_button = QPushButton(button_data['text'])
        update_button.clicked.connect(lambda _, data=button_data: data['action']())
        update_button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
                margin-left: 10px;
                border-radius: 4px;
                color: yellow;
            }
            QPushButton:hover {
                color: #333;
            }
            QPushButton:disabled {
                color: #333;
            }
        """)
        if not is_updateable:
            update_button.setEnabled(False)
        return update_button
    
    def _create_enable_button(self, profile, theme):
        is_enabled = installer.is_enabled(profile, theme)
        button_data = {
            'text': 'Disable' if is_enabled else 'Enable',
            'action': (lambda _=None, theme=theme, profile=profile, is_enabled=is_enabled:
                       (self._disable(theme, profile) if is_enabled else self._enable(theme, profile))),
            'color': 'blue' if is_enabled else 'green',
            'objectName': 'disableButton' if is_enabled else 'enableButton',
        }
        toggle_enable_button = QPushButton(button_data['text'])
        toggle_enable_button.clicked.connect(lambda _, data=button_data: data['action']())
        toggle_enable_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                padding: 5px;
                margin-left: 10px;
                border-radius: 4px;
                color: {button_data['color']};
            }}
            QPushButton:hover {{
                color: #333;
            }}
        """)
        
        return toggle_enable_button


    def resize(self, width):
        self.setFixedWidth(width)
        
    def resizeEvent(self, event: QResizeEvent):
        self.resize(event.size().width())
        super().resizeEvent(event)
    
    def _update(self, theme, profile):
        try:
            installer.update_theme(profile, theme)
            print(f"Theme {theme} updated in {profile}")
        except Exception as e:
            print(f"Error updating theme {theme}: {e}")
        self.update_themes()

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

    def _enable(self, theme, profile):
        try:
            installer.enable_theme(profile, theme)
            print(f"Theme {theme} enabled in {profile}")
        except Exception as e:
            print(f"Error enabling theme {theme}: {e}")
        self.update_themes()
        
    def _disable(self, theme, profile):
        try:
            installer.disable_theme(profile, theme)
            print(f"Theme {theme} disabled in {profile}")
        except Exception as e:
            print(f"Error disabling theme {theme}: {e}")
        self.update_themes()
