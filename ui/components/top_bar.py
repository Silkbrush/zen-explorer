from PySide6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QComboBox,
)
from zen_explorer_core.profiles import get_profile_path, get_profiles
from .styled_widget import StyledWidget

class TopBar(StyledWidget):
    def __init__(self, navui):
        super().__init__()
        self.setObjectName("TopBar")
        self.setProperty("type", "navigation")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)  # Zero horizontal margins
        self.main_layout.setSpacing(10) 
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
        self.install_btn.setObjectName('InstallButton')
        self.install_btn.setProperty('type', 'navbutton')
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
            button.setProperty('type', 'navbutton')
            self.navigator_layout.addWidget(button)
            button.clicked.connect(lambda _, i=i+1: self.show_screen(index=i))

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
        self.option_combo_box.setObjectName("ProfileSelector")
        
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