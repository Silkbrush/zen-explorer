from PySide6.QtGui import QResizeEvent, Qt
from PySide6.QtWidgets import QVBoxLayout, QComboBox, QLineEdit, QLabel, QHBoxLayout

from zen_explorer_core.settings import SettingsData, settings_definitions, SettingDefinition
from ..models.widgets import QWidget

class SettingsScreen(QWidget):
    def __init__(self, root, settings: SettingsData):
        super().__init__()
        self.settings = settings
        self.title_label = QLabel('Settings')
        self.title_label.setStyleSheet("font-weight: bold; font-size: 30px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label = QLabel(' - Restart to apply')
        self.subtitle_label.setStyleSheet("font-size: 20px;")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_layout = QHBoxLayout()
        self.label_layout.addStretch()
        self.label_layout.addWidget(self.title_label)
        self.label_layout.addWidget(self.subtitle_label)
        self.label_layout.addStretch()
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(10, 10, 10, 10)
        self._layout.addLayout(self.label_layout)
        self.setLayout(self._layout)
        self._create_settings()
        self.resize(root.width())
        self.setStyleSheet('color: white;')

    def _create_settings(self):
        for setting in settings_definitions.items():
            self._layout.addWidget(self._create_setting_widget(setting))

    def _create_setting_widget(self, setting_data: tuple[str, SettingDefinition]):
        setting_widget = QWidget()
        setting_widget.setStyleSheet("""
            QWidget {
                background-color: #222;
                border-radius: 10px;
                padding: 8px;
            }
        """)
        setting_layout = QHBoxLayout(setting_widget)
        setting_layout.setContentsMargins(10, 10, 10, 10)
        setting_widget.setLayout(setting_layout)
        setting = setting_data[1]
        print(setting)
        setting_label = setting['name']
        setting_label_widget = QLabel(setting_label)
        widget = QLabel('Couldn\'t create widget for this setting')
        if setting['type'] == 'select':
            select_widget = QComboBox()
            select_widget.addItems(setting['choices'])
            select_widget.setCurrentText(self.settings.get_setting(setting_data[0]))
            select_widget.setStyleSheet("""
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
            widget = select_widget
        elif setting['type'] == 'str':
            widget = QLineEdit()
        setting_layout.addWidget(setting_label_widget)
        setting_layout.addStretch()
        setting_layout.addWidget(widget)
        return setting_widget

    def resize(self, width):
        self.setFixedWidth(width)

    def resizeEvent(self, event: QResizeEvent):
        self.resize(event.size().width())
        super().resizeEvent(event)
