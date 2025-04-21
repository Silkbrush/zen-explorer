from enum import Enum
from datetime import datetime

from customtkinter import S

class ThemeType(Enum):
    bundle = 0
    chrome = 1
    content = 2

class Theme:
    def __init__(self, data: dict, install_data: dict, _id=None):
        self._raw_data: dict = data
        self._raw_install_data: dict = install_data
        self._id = _id
    
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._raw_data.get('name')

    @property
    def author(self) -> str:
        return self._raw_data.get('author')

    @property
    def type(self) -> ThemeType:
        return ThemeType(self._raw_data.get('type'))

    @property
    def type_name(self) -> str:
        if self.type == ThemeType.bundle:
            return 'bundle'
        elif self.type == ThemeType.chrome:
            return 'theme'
        elif self.type == ThemeType.content:
            return 'page'
        else:
            return 'unknown'

    @property
    def description(self) -> str:
        return self._raw_data.get('description')

    @property
    def author_url(self) -> str:
        return self._raw_data.get('authorUrl')

    @property
    def homepage(self) -> str:
        return self._raw_data.get('homepage')

    @property
    def version(self) -> str:
        return self._raw_data.get('version')

    @property
    def created_at(self) -> datetime:
        # convert unix time to datetime
        return datetime.fromtimestamp(self._raw_data.get('createdAt'))

    @property
    def updated_at(self) -> datetime:
        # convert unix time to datetime
        return datetime.fromtimestamp(self._raw_data.get('updatedAt'))

    @property
    def tags(self) -> list:
        return self._raw_data.get('tags')

    @property
    def files(self) -> list:
        return self._raw_install_data.get('files')

    @property
    def folders(self) -> list:
        return self._raw_install_data.get('folders')

    @property
    def chrome_targets(self) -> list:
        return self._raw_install_data.get('uclChromeTarget')

    @property
    def content_targets(self) -> list:
        return self._raw_install_data.get('uclContentTarget')

    @property
    def raw_install_data(self) -> dict:
        return self._raw_install_data
