import os
import sys
from pathlib import Path

home = str(Path.home())

def _get_macos_path():
    path = home + '/Library/Application Support/zen/Profiles'

    if not os.path.exists(path):
        raise FileNotFoundError('Zen Browser is not installed')

    return path

def _get_windows_path():
    raise RuntimeError('Windows is not supported yet')

def _get_linux_path():
    path = home + '/.zen/Profiles'

    if not os.path.exists(path):
        raise FileNotFoundError('Zen Browser is not installed')

    return path

def _get_flatpak_path():
    path = home + '/.var/app/app.zen_browser.zen/.zen'

    if not os.path.exists(path):
        raise FileNotFoundError('Zen Browser is not installed')

    return path

def get_profiles():
    os_name = sys.platform

    if os_name == 'darwin':
        paths = [_get_macos_path()]
    elif os_name == 'win32':
        paths = [_get_windows_path()]
    else:
        paths = []

        try:
            paths.append(_get_linux_path())
            paths.append(_get_flatpak_path())
        except:
            if not paths:
                raise

    profiles = []
    for path in paths:
        profiles.extend(os.listdir(path))

        for profile in profiles:
            # check if profile is a path
            if not os.path.exists(path + '/' + profile) or profile.startswith('.'):
                profiles.remove(profile)

    return profiles
