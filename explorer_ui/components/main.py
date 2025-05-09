from typing import Optional
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from zen_explorer_core import repository, profiles, installer
from zen_explorer_core.models import theme
from explorer_ui.components import topbar, content
from explorer_ui.models import pages, profiles as profile_models
from explorer_ui.pages import discover, overview, management
from explorer_ui.utils import images


class MainWindow(QMainWindow):
    def __init__(self, repo: repository.RepositoryData):
        super().__init__()

        # Set window properties
        self.resize(800, 600)
        self.setWindowTitle("Silkthemes")
        self.setStyleSheet('background-color: #333;')

        # Create widget and layout
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        # Remove borders
        self.widget.setStyleSheet('border: 0;')
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Set widgets
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.layout)

        # Add repo data
        self.repository: repository.RepositoryData = repo

        # Add profiles list
        self.profiles: list = []
        for profile in profiles.get_profiles():
            try:
                self.profiles.append(profile_models.Profile.from_string(profile))
            except ValueError:
                pass

        # Window components
        self.topbar: Optional[topbar.TopBar] = None
        self.content: Optional[content.Content] = None
        self.current_screen: Optional[QWidget] = None

        # Window variables
        self.page: pages.Pages = pages.Pages.discover
        self.profile: profile_models.Profile = self.profiles[0]
        self.theme: Optional[theme.Theme] = None
        self.thumbnails = {}
        self.default_thumbnail = images.get_pixmap(
            'https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png'
        )

        # Internal variables
        self.__ready = False

    def prepare(self):
        """Prepares the window for use."""

        # Do not run if already prepared
        if self.__ready:
            raise RuntimeError("window is already prepared")

        # Load topbar
        self.topbar = topbar.TopBar(self)
        self.layout.addWidget(self.topbar)

        # Load sidebar
        # TODO: implement sidebar

        # Load content
        self.content = content.Content(self)
        self.layout.addWidget(self.content)

        # Prepare topbar, sidebar and content
        self.topbar.prepare()
        self.content.prepare()
        self.content.set_content(discover.ThemeBrowseScreen(self))

        # Set ready status
        self.__ready = True
    
    def get_current_page(self):
        return self.page

    def get_current_page_content(self):
        return self.content.get_content()

    def navigate(self, page: pages.Pages):
        # wip
        print(f'Navigating: {self.page} => {page}')
        self.page = page
        self.topbar.handle_page_update()

        if page == pages.Pages.discover:
            screen = discover.ThemeBrowseScreen(self)
        elif page == pages.Pages.overview:
            screen = overview.ThemeScreen(self)
        elif page == pages.Pages.manage:
            screen = management.ThemeManagementScreen(self)
        self.current_screen = screen
        self.content.set_content(screen)

        self.content.resize()

    def install(self):
        try:
            print(f'Staging installing {self.theme.name} by {self.theme.author}...')
            installer.install_theme(
                f'{self.profile.id}.{self.profile.name}', self.theme.id, staging=True, bypass_install=True
            )
            print('Staging passed successfully')
            print(f'Installing {self.theme.name} by {self.theme.author}...')
            installer.install_theme(
                f'{self.profile.id}.{self.profile.name}', self.theme.id, bypass_install=True
            )
            print('Installed successfully')
        except Exception as e:
            # TODO: add banners sometime later for this
            print('Failed to install theme: ', e)
        else:
            pass

    def uninstall(self):
        try:
            print(f'Staging uninstalling {self.theme.name} by {self.theme.author}...')
            installer.uninstall_theme(
                f'{self.profile.id}.{self.profile.name}', self.theme.id, staging=True
            )
            print('Staging passed successfully')
            print(f'Uninstalling {self.theme.name} by {self.theme.author}...')
            installer.uninstall_theme(
                f'{self.profile.id}.{self.profile.name}', self.theme.id
            )
            print('Uninstalled successfully')
        except Exception as e:
            print('Failed to uninstall theme: ', e)
        else:
            pass

    def resizeEvent(self, event):
        self.content.resizeEvent(event)
        super().resizeEvent(event)
