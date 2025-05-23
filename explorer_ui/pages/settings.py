from PySide6.QtWidgets import QVBoxLayout, QComboBox, QLineEdit, QLabel, QHBoxLayout

from zen_explorer_core.settings import SettingsData, settings_definitions, SettingDefinition
from ..models.widgets import QWidget

class SettingsScreen(QWidget):
    def __init__(self, root, settings: SettingsData):
        super().__init__()
        self.settings = settings
        self._layout = QVBoxLayout()
        self._create_settings()
        self.setLayout(self._layout)

    def _create_settings(self):
        for setting in settings_definitions.items():
            self._layout.addWidget(self._create_setting_widget(setting))

    def _create_setting_widget(self, setting_data: tuple[str, SettingDefinition]):
        setting_widget = QWidget()
        setting_layout = QHBoxLayout()
        setting_widget.setLayout(setting_layout)
        setting = setting_data[1]
        print(setting)
        setting_label = setting['name']
        setting_label_widget = QLabel(setting_label)
        setting_layout.addWidget(setting_label_widget)
        widget = QLabel('Couldn\'t create widget for this setting')
        if setting['type'] == 'select':
            select_widget = QComboBox()
            select_widget.addItems(setting['choices'])
            select_widget.setCurrentText(self.settings.get_setting(setting_data[0]))
            widget = select_widget
        elif setting['type'] == 'str':
            widget = QLineEdit()

        setting_layout.addWidget(widget)
        return setting_widget
