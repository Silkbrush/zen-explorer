import os
import json
import shutil
from typing import Optional
from zen_explorer_core import profiles, repository
from zen_explorer_core.models import theme

zen_profiles = profiles.get_profiles()

def _profile_exists(profile):
    if not profile in zen_profiles:
        for profile_name in zen_profiles:
            if profile == profile_name.split('.', 1)[0]:
                return profile_name
        raise NotADirectoryError('invalid profile')
    else:
        return profile

def _build_css(data):
    chrome_lines = []
    content_lines = []
    for zen_theme in data:
        for target in data[zen_theme]['uclChromeTarget']:
            chrome_lines.append(f'@import url("zen-explorer-themes/{zen_theme}/{target}");')
        for target in data[zen_theme]['uclContentTarget']:
            content_lines.append(f'@import url("zen-explorer-themes/{zen_theme}/{target}");')

    return '\n'.join(chrome_lines), '\n'.join(content_lines)

def _apply_css(path, data):
    chrome, content = _build_css(data)

    with open(f'{path}/chrome/userChrome.css', 'w+') as f:
        f.write(chrome)

    with open(f'{path}/chrome/userContent.css', 'w+') as f:
        f.write(content)

def _profile_path(profile):
    return profiles.get_profile_path(profile)

def check_userchrome(profile):
    profile = _profile_exists(profile)
    path = _profile_path(profile)

    return os.path.isdir(f'{path}/chrome') and os.path.isfile(f'{path}/chrome/userChrome.css')

def check_usercontent(profile):
    profile = _profile_exists(profile)
    path = _profile_path(profile)

    return os.path.isdir(f'{path}/chrome') and os.path.isfile(f'{path}/chrome/userContent.css')

def check_installed(profile):
    profile = _profile_exists(profile)
    path = _profile_path(profile)

    return os.path.isdir(f'{path}/chrome') and os.path.isfile(f'{path}/chrome/zen-explorer.json')

def install_theme(profile, theme_id, bypass_install=False, staging=False):
    profile = _profile_exists(profile)
    if (check_userchrome(profile) or check_usercontent(profile)) and not check_installed(profile) and not bypass_install:
        raise RuntimeError('userchrome or usercontent already exists, set bypass_install to True to bypass')

    zen_theme: Optional[theme.Theme] = repository.data.get_theme(theme_id)
    if not zen_theme:
        raise FileNotFoundError('theme not found')

    if not check_installed(profile):
        new_data = {}
    else:
        with open(f'{_profile_path(profile)}/chrome/zen-explorer.json', 'r') as f:
            new_data = json.load(f)

    new_data[theme_id] = {
        'version': zen_theme.version,
        'updatedAt': zen_theme.updated_at.timestamp(),
        'uclChromeTarget': zen_theme.chrome_targets,
        'uclContentTarget': zen_theme.content_targets
    }

    if not staging:
        if not os.path.isdir(f'{_profile_path(profile)}/chrome'):
            os.makedirs(f'{_profile_path(profile)}/chrome')
        if not os.path.isdir(f'{_profile_path(profile)}/chrome/zen-explorer-themes'):
            os.makedirs(f'{_profile_path(profile)}/chrome/zen-explorer-themes')

    if staging:
        print('Simulated data update')
        print(new_data)
    else:
        with open(f'{_profile_path(profile)}/chrome/zen-explorer.json', 'w+') as f:
            # noinspection PyTypeChecker
            json.dump(new_data, f, indent=4)

    theme_path = f'{repository.repository_path()}/themes/{theme_id}'
    profile_path = _profile_path(profile)

    # Replace theme path with a simulated data copy
    if not staging:
        if os.path.isdir(f'{profile_path}/chrome/zen-explorer-themes/{theme_id}'):
            shutil.rmtree(f'{profile_path}/chrome/zen-explorer-themes/{theme_id}')
        os.makedirs(f'{profile_path}/chrome/zen-explorer-themes/{theme_id}')

    for file in zen_theme.files:
        if staging:
            print(f'Simulated data copy: {theme_path}/{file} => {profile_path}/chrome/zen-explorer-themes/{theme_id}/{file}')
        else:
            shutil.copy2(f'{theme_path}/{file}', f'{profile_path}/chrome/zen-explorer-themes/{theme_id}/{file}')

    for folder in zen_theme.folders:
        if staging:
            print(f'Simulated data copy: {theme_path}/{folder} => {profile_path}/chrome/zen-explorer-themes/{theme_id}/{folder}')
        else:
            shutil.copytree(f'{theme_path}/{folder}', f'{profile_path}/chrome/zen-explorer-themes/{theme_id}/{folder}')

    # We can overwrite userChrome and userContent here
    if staging:
        chrome, content = _build_css(new_data)
        print('Simulated chrome write')
        print(chrome)
        print('\nSimulated content write')
        print(content)
    else:
        _apply_css(profile_path, new_data)

def uninstall_theme(profile, theme_id, staging=False):
    profile = _profile_exists(profile)
    if not check_installed(profile):
        raise RuntimeError('not installed')

    profile_path = _profile_path(profile)

    with open(f'{profile_path}/chrome/zen-explorer.json', 'r') as f:
        data = json.load(f)

    if not theme_id in data:
        raise FileNotFoundError('theme not installed')

    if staging:
        print(f'Simulated data removal of {profile_path}/chrome/zen-explorer-themes/{theme_id}')
    else:
        try:
            shutil.rmtree(f'{profile_path}/chrome/zen-explorer-themes/{theme_id}')
        except FileNotFoundError:
            pass

    del data[theme_id]

    if staging:
        print('Simulated data update')
    else:
        with open(f'{profile_path}/chrome/zen-explorer.json', 'w+') as f:
            # noinspection PyTypeChecker
            json.dump(data, f, indent=4)

    # We can overwrite userChrome and userContent here
    if staging:
        chrome, content = _build_css(data)
        print('Simulated chrome write')
        print(chrome)
        print('\nSimulated content write')
        print(content)
    else:
        _apply_css(profile_path, data)

def get_updates(profile) -> dict:
    profile = _profile_exists(profile)
    if not check_installed(profile):
        raise RuntimeError('not installed')

    profile_path = _profile_path(profile)

    with open(f'{profile_path}/chrome/zen-explorer.json', 'r') as f:
        data = json.load(f)

    updates = {}
    for theme_id in data:
        zen_theme: Optional[theme.Theme] = repository.data.get_theme(theme_id)
        if not zen_theme:
            continue

        if zen_theme.updated_at > data[theme_id]['updatedAt']:
            updates[theme_id] = zen_theme

    return updates
