import os
import sys
import traceback
from pathlib import Path

home = str(Path.home())

def _get_macos_path():
    path = home + '/Library/Application Support/zen/Profiles'

    if not os.path.exists(path):
        raise NotADirectoryError('Zen Browser is not installed')

    return path

def _get_windows_path():
    path = home + '/AppData/Roaming/zen/Profiles'

    if not os.path.exists(path):
        raise NotADirectoryError('Zen Browser is not installed')

    return path

def _get_linux_path():
    zen_path = home + '/.zen'
    path = home + '/.zen/Profiles'
    
    if os.path.exists(zen_path):
        if os.path.exists(path):
            return path
        
        else:
            if os.path.exists(zen_path):
                return zen_path
            
    raise NotADirectoryError('Zen Browser is not installed')

    

def _get_flatpak_path():
    path = home + '/.var/app/app.zen_browser.zen/.zen'

    if not os.path.exists(path):
        raise NotADirectoryError('Zen Browser is not installed')

    return path

def _get_paths():
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

def get_profiles():
    paths = _get_paths()
    print(f'\nChecking for profiles in {paths}')
    print(f'path content: {[path for path in paths]}')
    profiles = []
    for path in paths:
        profiles.extend(os.listdir(path))

        for profile in profiles:
            print(f'\nfound possible profile: {profile}')
            # check if profile is a path
            if not os.path.isdir(f'{path}/{profile}') or profile.startswith('.'):
                print(f'removing invalid profile: {profile}')
                profiles.remove(profile)
            else:
                try: 
                    profile_id, profile_name = profile.split('.', 1)
                    print(f'adding valid profile: {profile}')
                except ValueError:
                    print(f'There seem to have been a non-profile file or folder inside the profiles directory. Skipping this profile: {profile}.')
                    profiles.remove(profile)
                            

    return profiles
