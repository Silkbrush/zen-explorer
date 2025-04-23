from typing import Optional
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from zen_explorer_core import repository, profiles, installer
from zen_explorer_core.models import theme
from explorer_ui.components import topbar, content
from explorer_ui.models import pages, profiles as profile_models
from explorer_ui.pages import discover, overview


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

        # Window variables
        self.page: pages.Pages = pages.Pages.discover
        self.profile: profile_models.Profile = self.profiles[0]
        self.theme: Optional[theme.Theme] = None

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

    def navigate(self, page: pages.Pages):
        # wip
        print(f'Navigating: {self.page} => {page}')
        self.page = page
        self.topbar.handle_page_update()

        if page == pages.Pages.discover:
            self.content.set_content(discover.ThemeBrowseScreen(self))
        elif page == pages.Pages.overview:
            self.content.set_content(overview.ThemeScreen(self))

        self.content.resize()

    def install(self):
        try:
            print(f'Staging installing {self.theme.name} by {self.theme.author}...')
            installer.install_theme(
                f'{self.profile.id}.{self.profile.name}', self.theme.id, staging=True
            )
            print('Staging passed successfully')
            print(f'Installing {self.theme.name} by {self.theme.author}...')
            installer.install_theme(
                f'{self.profile.id}.{self.profile.name}', self.theme.id
            )
            print('Installed successfully')
        except Exception as e:
            # TODO: add banners sometime later for this
            print('Failed to install theme: ', e)
        else:
            pass

    def resizeEvent(self, event):
        self.content.resizeEvent(event)
        super().resizeEvent(event)
