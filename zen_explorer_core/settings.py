import json
import os
from typing import Optional, TypedDict, NotRequired, Union

import platformdirs

save_dir = os.environ.get('WORKING_DIR') or platformdirs.user_data_dir('zen-explorer')

class SettingDefinition(TypedDict):
    name: str
    type: str
    choices: NotRequired[list[str]]
    description: str
    default: str

SettingDefinitions = dict[str, SettingDefinition]

class SettingValue(TypedDict):
    value: Union[str, bool]

SettingValues = dict[str, SettingValue]

settings: SettingDefinitions = {  # This just sets what settings exist. This will be used for loading the UI. The
    'application theme': {  # actual settings will be a JSON formatted like SettingValues
        'name': 'Application theme',
        'type': 'select',
        'choices': ['dark', 'light'],
        'description': 'Change the appearance of the application.',
        'default': 'dark'
    },
    'standard browser': {
        'name': 'Standard browser',
        'type': 'select',
        'choices': ['zen', 'firefox'],
        'description': 'Change the default browser.',
        'default': 'zen'
    }
}

class SettingsData:
    def __init__(self, path):
        self._path = path
        self._data = {}

        if os.path.isfile(f'{self._path}/settings.json'):
            with open(f'{self._path}/settings.json', 'r') as f:
                self._data.update(json.load(f))
        else:
            print('settings.json not found in repository directory, creating...')
            with open(f'{self._path}/settings.json', 'w') as f:
                f.close()

    def get_setting(self, key):
        return self._data.get(key)

    def set_setting(self, key, value):
        try:
            self._data[key] = value
            with open(f'{self._path}/settings.json', 'w') as f:
                f.write(json.dumps(self._data))

        except KeyError:
            print(f'setting {key} not found')

    def get_settings(self):
        return self._data

data: Optional[SettingsData] = None