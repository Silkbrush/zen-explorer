import os
from typing_extensions import Literal, Union, TypedDict
from pathlib import Path
import sys

home = str(Path.home())
browsers = ["zen", "firefox"]
browser: Union[Literal["zen"], Literal["firefox"]] = "zen"

class BrowserPath(TypedDict):
    macos: list[str]
    windows: list[str]
    linux: list[str]
    flatpak: list[str]

BrowserPaths = dict[str, BrowserPath]

paths: BrowserPaths = {
    'zen': {
        'macos': [home + '/Library/Application Support/zen/Profiles'],
        'windows': [home + '/AppData/Roaming/zen/Profiles'],
        'linux': [home + '/.zen/Profiles', home + '/.zen'],
        'flatpak': [home + '/.var/app/app.zen_browser.zen/.zen'],
    },
    'firefox': {
        'macos': [home + '/Library/Application Support/Firefox/Profiles'],
        'windows': [home + '/AppData/Roaming/Mozilla/Firefox/Profiles'],
        'linux': [home + '/.mozilla/firefox'],
        'flatpak': [home + '/.var/app/org.mozilla.firefox/.mozilla/firefox'],
    }
}

def _get_macos_path():
    for path in paths[browser]['macos']:
        if os.path.exists(path):
            yield path


def _get_windows_path():
    for path in paths[browser]['windows']:
        if os.path.exists(path):
            yield path


def _get_linux_path():
    for path in paths[browser]['linux']:
        if os.path.exists(path):
            yield path
            
    raise NotADirectoryError('Zen Browser is not installed')


def _get_flatpak_path():
    for path in paths[browser]['flatpak']:
        if os.path.exists(path):
            yield path

    raise NotADirectoryError('Zen Browser is not installed')

def _get_paths():
    os_name = sys.platform
    paths = []
    if os_name == 'darwin':
        paths.extend(_get_macos_path())
    elif os_name == 'win32':
        paths.extend(_get_windows_path())
    else:
        try:
            paths.extend(_get_flatpak_path())
        except Exception:
            pass
        try:
            paths.extend(_get_linux_path())
        except Exception:
            if not paths:
                raise

    return paths