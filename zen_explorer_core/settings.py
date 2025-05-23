import json
import os
from typing import Optional, TypedDict, NotRequired, Union, Any, Literal

import platformdirs

save_dir = os.environ.get('WORKING_DIR') or platformdirs.user_data_dir('zen-explorer')

class SettingDefinition(TypedDict):
    name: str
    type: Union[Literal['select'], Literal['number'], Literal['string'], Literal['boolean']]
    select_type: NotRequired[Any]
    choices: NotRequired[list[str]]
    description: str
    default: str

SettingDefinitions = dict[str, SettingDefinition]

SettingValues = dict[str, Union[str, bool, int]]

settings_definitions: SettingDefinitions = {  # This just sets what settings exist. This will be used for loading the UI. The
    'application theme': {        # actual settings will be a JSON formatted like SettingValues.
        'name': 'Application theme',
        'type': 'select',
        'select_type': str,
        'choices': ['dark', 'light'],
        'description': 'Change the appearance of the application.',
        'default': 'dark'
    },
    'standard browser': {
        'name': 'Standard browser',
        'type': 'select',
        'select_type': str,
        'choices': ['zen', 'firefox'],
        'description': 'Change the default browser.',
        'default': 'zen'
    },
    'themes per page': {
        'name': 'Themes per page',
        'type': 'number',
        'description': 'Change the number of themes per page.',
        'default': '20'
    }
}

settingtype2type = {
    'select': Any,
    'number': int,
    'string': str,
    'boolean': bool,
}


class SettingsData:
    def __init__(self, path):
        self._path = path
        self._data = {}

        if os.path.isfile(f'{self._path}/settings.json'):
            with open(f'{self._path}/settings.json', 'r') as f:
                self._data.update(json.load(f))
        else:
            self._create_settings_file()
        self._update_settings_file()

    def _update_settings_file(self):
        if os.path.isfile(f'{self._path}/settings.json'):
            with open(f'{self._path}/settings.json', 'r') as f:
                settings_data: SettingValues = json.load(f)
                settings_data.update(self._data)
                for key, value in settings_definitions.items():
                    if not key in settings_data:
                        settings_data[key] = value['default']
                for key, value in settings_data.items():
                    if not key in settings_definitions:
                        del settings_data[key]
                self._data = settings_data
                with open(f'{self._path}/settings.json', 'w') as f:
                    f.write(json.dumps(self._data))
        else:
            self._create_settings_file()
            self._update_settings_file()

    def _create_settings_file(self):
        if not os.path.isfile(f'{self._path}/settings.json'):
            with open(f'{self._path}/settings.json', 'w') as f:
                f.write(json.dumps(self._data))
        else:
            print('settings.json already exists')

    def get_setting(self, key):
        return self._data.get(key)

    def set_setting(self, key, value):
        try:
            if get_setting_type(key) == value.__class__:
                self._data[key] = value
            with open(f'{self._path}/settings.json', 'w') as f:
                f.write(json.dumps(self._data))

        except KeyError:
            print(f'setting {key} not found')

    def get_settings(self):
        return self._data

def setting_exists(key):
    return key in settings_definitions

def get_settings_path():
    return save_dir

def load_settings():
    global settings
    settings = SettingsData(save_dir)

def get_setting_type(key):
    if key in settings_definitions:
        setting_type = settings_definitions[key]['type']
        return settingtype2type[setting_type] if setting_type != 'select' else settings_definitions[key]['select_type']
    else:
        return str

settings: Optional[SettingsData] = None