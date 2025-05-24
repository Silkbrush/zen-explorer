from typing import TYPE_CHECKING, Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QComboBox

from explorer_ui.models import pages
from explorer_ui.models.widgets import QWidget
from explorer_ui.utils import widgets
from zen_explorer_core import browser, installer, profiles

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
        self.search_area = QHBoxLayout()
        self.wrapper_area.addLayout(self.navigation_area)
        self.wrapper_area.addLayout(self.search_area)
        self.wrapper_area.addLayout(self.profile_area)


        # Align areas
        self.navigation_area.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.profile_area.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.search_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        for button in self._create_navigation_buttons():
            self.navigation_area.addWidget(button)
            self.__widgets.add_widget(button)

        for button in self._create_profile_buttons():
            self.profile_area.addWidget(button)
            self.__widgets.add_widget(button)
            
        browser_selector = self._create_browser_selelector()
        self.profile_area.addWidget(browser_selector)
        self.__widgets.add_widget(browser_selector)
        profile_selector = self._create_profile_selector()
        self.profile_area.addWidget(profile_selector)
        self.__widgets.add_widget(profile_selector)
        self._root.profile = self._profiles[0]
        

        # Run update
        self._update_buttons()

    def _create_navigation_buttons(self):
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
                    color: white;
                }

                QPushButton[active] {
                    background-color: #3498db;
                }
            """)
            # self.__widgets.add_widget(button)
            # self.navigation_area.addWidget(button)
            yield button

    def _create_profile_buttons(self):
        # Add install button to profile area
        install_button = QPushButton('Install')
        install_button.setObjectName('buttonInstall')
        install_button.clicked.connect(self._install)
        install_button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
                margin-left: 10px;
                border-radius: 4px;
                color: white;
            }

            QPushButton[active] {
                background-color: #3498db;
            }
        """)
        # self.profile_area.addWidget(install_button)
        # self.__widgets.add_widget(install_button)
        yield install_button

        # Add uninstall button to profile area
        uninstall_button = QPushButton('Uninstall')
        uninstall_button.setObjectName('buttonUninstall')
        uninstall_button.clicked.connect(self._uninstall)
        uninstall_button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
                margin-left: 10px;
                border-radius: 4px;
                color: white;
                background-color: #e74c3c;
            }

            QPushButton[active] {
                background-color: #3498db;
            }
        """)
        # self.profile_area.addWidget(uninstall_button)
        # self.__widgets.add_widget(uninstall_button)
        yield uninstall_button

    def _create_profile_selector(self):
        # Add profile selector
        choices = [f'{profile.name} ({profile.id})' for profile in self._profiles]
        profile_selector = QComboBox()
        profile_selector.setObjectName('profileSelector')
        profile_selector.addItems(choices)
        profile_selector.setCurrentIndex(0)
        profile_selector.currentIndexChanged.connect(self._update_selected_profile)
        profile_selector.setStyleSheet("""
            QComboBox {
                border: none;
                padding: 5px;
                margin-left: 10px;
                border-radius: 4px;
                color: white;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                border-left: none; /* Remove the border between the field and drop-down */
                background: transparent; /* Remove background of the drop-down */
                image: url('explorer_ui/assets/icons/down-arrow-white.png');
                width: 8px;
                height: 8px;
                margin-right: 5px;
            }

            QComboBox QAbstractItemView {
                margin: 0;
                padding: 0;
                background-color: #222;
            }
        """)
        return profile_selector

    def _create_browser_selelector(self):
        global browser
        browsers = browser.browsers
        choices = [browser for browser in browsers]
        browser_selector = QComboBox()
        browser_selector.setObjectName('browserSelector')
        browser_selector.addItems(choices)
        browser_selector.setCurrentText(browser.browser)
        browser_selector.currentIndexChanged.connect(self._update_selected_browser)
        browser_selector.setStyleSheet("""
            QComboBox {
                border: none;
                padding: 5px;
                margin-left: 10px;
                border-radius: 4px;
                color: white;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                border-left: none; /* Remove the border between the field and drop-down */
                background: transparent; /* Remove background of the drop-down */
                image: url('explorer_ui/assets/icons/down-arrow-white.png');
                width: 8px;
                height: 8px;
                margin-right: 5px;
            }

            QComboBox QAbstractItemView {
                margin: 0;
                padding: 0;
                background-color: #222;
            }
        """)
        return browser_selector

    def _create_search_bar(self):
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.textChanged.connect(lambda _: self._search(self.search_bar.text()))
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: #fff;
                border: none;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        self.search_area.addWidget(self.search_bar)

    def _search(self, query):
        if self._root.get_current_page() == pages.Pages.discover:
            self._root.get_current_page_content().search(query)

    def _update_search_bar(self):
        if self._root.get_current_page() == pages.Pages.discover:
            self.search_bar.show()
            self.search_bar.setFocus()
            print("Search bar shown")
        else:
            self.search_bar.hide()
            print("Search bar hidden")

    def _update_buttons(self):
        """Internal function to update existing buttons."""

        for button in self._btn_pages:
            button_obj = self.__widgets.get_widget(button)
            if self._root.get_current_page() == self._btn_pages[button]:
                button_obj.setProperty("active", "true")
            else:
                button_obj.setProperty("active", None)
            button_obj.setStyleSheet(button_obj.styleSheet())

        # If not on overview page, hide install button
        install_button = self.__widgets.get_widget('buttonInstall')
        uninstall_button = self.__widgets.get_widget('buttonUninstall')
        if self._root.get_current_page() == pages.Pages.overview:
            # Check if theme is installed
            theme = self._root.theme
            print(f'Checking if {theme.id} is installed in {self._root.profile.id}.{self._root.profile.name} in the browser {browser.browser}...')
            installed = installer.is_installed(
                f'{self._root.profile.id}.{self._root.profile.name}', theme.id
            )

            if installed:
                uninstall_button.show()
                install_button.hide()
            else:
                install_button.show()
                uninstall_button.hide()
        else:
            install_button.hide()
            uninstall_button.hide()

    # Prepare method
    def prepare(self):
        """Prepares the widget for use."""

        # Do not run if already prepared
        if self.__ready:
            raise RuntimeError('widget is already prepared')

        # Create buttons
        self._create_buttons()
        self._create_search_bar()

        # Set ready state
        self.__ready = True

    # Event methods (local)
    def _update_selected_profile(self, index: int):
        # Update selected profile
        if index < 0 or index >= len(self._profiles):
            self._root.profile = self._profiles[0]
        else:
            self._root.profile = self._profiles[index]

        self._update_buttons()

        print(f'Selected profile: {self._root.profile.name} ({self._root.profile.id})')

    def _update_profile_switcher(self):
        switcher = self.__widgets.get_widget('profileSelector')
        
        # Clear existing items in the selector
        switcher.clear()
        
        # Add new items based on updated profiles
        choices = [f'{profile.name} ({profile.id})' for profile in self._profiles]
        switcher.addItems(choices)
        
        # Set to first profile if available
        if self._profiles:
            switcher.setCurrentIndex(0)
            self._root.profile = self._profiles[0]
        
        

    def _update_selected_browser(self, index: int):
        # Update selected profile
        if index > 0 or index <= len(self._profiles):
            print(browser.browsers[index])
            browser.browser = browser.browsers[index]

        self._root.update_content()
        self._root.get_profiles()
        self._profiles = self._root.profiles
        self._update_profile_switcher()

        print(f'Selected profile: {self._root.profile.name} ({self._root.profile.id})')

    def _install(self):
        self._root.install()
        self._update_buttons()

    def _uninstall(self):
        self._root.uninstall()
        self._update_buttons()

    # Event methods (global)
    def handle_page_update(self):
        # Update buttons
        self._update_buttons()
        self._update_search_bar()