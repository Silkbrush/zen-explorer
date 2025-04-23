from PySide6.QtWidgets import QPushButton, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt
from explorer_ui.models import pages
from explorer_ui.models.widgets import QWidget
from explorer_ui.utils import widgets
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from explorer_ui.components.main import MainWindow
else:
    MainWindow = Any

class TopBar(QWidget):
    def __init__(self, root: MainWindow):
        super().__init__()
        self._root: MainWindow = root

        # Set object properties
        self.setObjectName("topBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #222; margin: 10px; margin-bottom: 0; border: none; border-radius: 6px;')
        self.setFixedHeight(60)

        # Create wrapper
        self.wrapper_area = QHBoxLayout(self)
        self.wrapper_area.setSpacing(0)

        # Create and add widget areas
        self.navigation_area = QHBoxLayout()
        self.profile_area = QHBoxLayout()
        self.wrapper_area.addLayout(self.navigation_area)
        self.wrapper_area.addLayout(self.profile_area)

        # Align areas
        self.navigation_area.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.profile_area.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Button names + behaviors
        self._behaviors: dict = {
            'Discover': lambda: self._root.navigate(pages.Pages.discover),
            'Manage': lambda: self._root.navigate(pages.Pages.manage),
            'Settings': lambda: self._root.navigate(pages.Pages.settings)
        }

        # Button pages
        self._btn_pages: dict = {
            'buttonDiscover': pages.Pages.discover,
            'buttonManage': pages.Pages.manage,
            'buttonSettings': pages.Pages.settings
        }

        # Shortcut for app.MainWindow.profiles
        self._profiles: list = self._root.profiles

        # Internal variables
        self.__ready: bool = False
        self.__widgets: widgets.WidgetHandler = widgets.WidgetHandler()

    def _create_buttons(self):
        """Internal function to create buttons."""

        # Clear buttons if any exist
        for i in reversed(range(self.navigation_area.count())):
            self.navigation_area.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.profile_area.count())):
            self.profile_area.itemAt(i).widget().deleteLater()

        # Add buttons to navigation area
        for name, behavior in self._behaviors.items():
            button = QPushButton(name)
            button.setObjectName('button'+name)
            button.clicked.connect(behavior)
            button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
                margin-left: 10px;
                border-radius: 4px;
            }
            
            QPushButton[active] {
                background-color: #3498db;
            }
            """)
            self.__widgets.add_widget(button)
            self.navigation_area.addWidget(button)

        # Add install button to profile area
        install_button = QPushButton('Install')
        install_button.setObjectName('buttonInstall')
        install_button.clicked.connect(self._install)
        self.profile_area.addWidget(install_button)
        self.__widgets.add_widget(install_button)

        # Add profile selector
        choices = [f'{profile.name} ({profile.id})' for profile in self._profiles]
        profile_selector = QComboBox()
        profile_selector.setObjectName('profileSelector')
        profile_selector.addItems(choices)
        profile_selector.setCurrentIndex(0)
        profile_selector.currentIndexChanged.connect(self._update_selected_profile)
        self.profile_area.addWidget(profile_selector)
        self._root.profile = self._profiles[0]

        # Run update
        self._update_buttons()

    def _update_buttons(self):
        """Internal function to update existing buttons."""

        for button in self._btn_pages:
            button_obj = self.__widgets.get_widget(button)
            if self._root.page == self._btn_pages[button]:
                button_obj.setProperty("active", "true")
            else:
                button_obj.setProperty("active", None)
            button_obj.setStyleSheet(button_obj.styleSheet())

        # If not on overview page, hide install button
        install_button = self.__widgets.get_widget('buttonInstall')
        if self._root.page == pages.Pages.overview:
            install_button.show()
        else:
            install_button.hide()

    # Prepare method
    def prepare(self):
        """Prepares the widget for use."""

        # Do not run if already prepared
        if self.__ready:
            raise RuntimeError('widget is already prepared')

        # Create buttons
        self._create_buttons()

        # Set ready state
        self.__ready = True

    # Event methods (local)
    def _update_selected_profile(self, index: int):
        # Update selected profile
        if index < 0 or index >= len(self._profiles):
            self._root.profile = self._profiles[0]
        else:
            self._root.profile = self._profiles[index]

        print(f'Selected profile: {self._root.profile.name} ({self._root.profile.id})')

    def _install(self):
        self._root.install()

    # Event methods (global)
    def handle_page_update(self):
        # Update buttons
        self._update_buttons()
