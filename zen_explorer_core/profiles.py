import json
import os
import sys
from pathlib import Path
from typing_extensions import Optional, Union, Literal


home = str(Path.home())
browsers = ["zen", "firefox"]
browser: Union[Literal["zen"], Literal["firefox"]] = "firefox"
paths = {
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

def get_profile_path(profile):
    paths = _get_paths()
    for path in paths:
        if os.path.isdir(f'{path}/{profile}'):
            return f'{path}/{profile}'

    raise NotADirectoryError('invalid profile')
    
def get_installed(profile) -> list[Optional[str]]:
    installed = []
    try:
        with open(f'{get_profile_path(profile)}/chrome/zen-explorer.json', 'r') as f:
            data = json.load(f)
            for theme in data.keys():
                installed.append(theme)
    except Exception:
        print(f"Error occurred while reading installed themes for profile {profile} at '{get_profile_path(profile)}/chrome/zen-explorer.json'")
    return installed

def get_profiles():
    """
    Retrieve a list of profile directory names.

    Returns:
        list: A list of strings representing the *names* of valid profile directories.
    """
    paths = _get_paths()
    profiles = []
    profile_includes_dirs = ['storage', 'extension-store']  # Example list of required directories
    for path in paths:
        possible_profiles = os.listdir(path)

        for profile in possible_profiles:
            if os.path.isdir(f'{path}/{profile}') and not profile.startswith('.') and not profile.endswith('.ini'):
                # Check if all required directories are present within the profile
                if all(os.path.isdir(f'{path}/{profile}/{req_dir}') for req_dir in profile_includes_dirs):
                    profiles.append(profile)

    return profiles
