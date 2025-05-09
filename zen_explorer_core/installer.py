import re
import os
import json
import shutil
from typing import Optional
from zen_explorer_core import profiles, repository
from zen_explorer_core.models import theme

zen_profiles = profiles.get_profiles()


def _extract_ids_from_css(file_path):
    """
    Parses a CSS file to extract specific IDs from @import rules.

    Args:
        file_path (str): The path to the CSS file.

    Returns:
        list: A list of tuples, where each tuple contains the
              line number (0-based) and the extracted ID.
              Returns an empty list if the file doesn't exist or
              no matching lines are found.
        str: An error message if the file cannot be read.
    """
    results = []
    # Regex to match @import url("zen-explorer-themes/(some-id)/...") and capture the ID
    pattern = re.compile(r'^@import\s+url\("zen-explorer-themes/([^/]+).*\);$')

    if not os.path.exists(file_path):
        return f"Error: File not found at '{file_path}'"
    if not os.path.isfile(file_path):
         return f"Error: Path '{file_path}' is not a file."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f): # Start count from 0
                stripped_line = line.strip()
                match = pattern.match(stripped_line)
                if match:
                    extracted_id = match.group(1)
                    results.append((extracted_id, line_num))
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"
    return results

def _profile_path(profile):
    return profiles.get_profile_path(profile)

def _profile_exists(profile):
    if profile not in zen_profiles:
        for profile_name in zen_profiles:
            if profile == profile_name.split('.', 1)[0]:
                return profile_name
        raise NotADirectoryError('invalid profile')
    else:
        return profile

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

def get_enabled_themes(profile) -> list[str]:
    """
    Retrieves a list of current theme IDs applied to the given user profile.

    Args:
        profile (str): The profile identifier to check for currently
        installed themes. (Format: <id>.<name>)

    Returns:
        list[str]: A list of theme IDs currently applied. If the profile is not installed,
        raises a RuntimeError.

    Raises:
        RuntimeError: If the profile is not installed or applicable chrome
        and content files don't exist.
    """
    profile = _profile_exists(profile)
    if not check_installed(profile):
        raise RuntimeError('not installed')

    profile_path = _profile_path(profile)
    css_path = f'{profile_path}/chrome/silkthemes-chrome.css'
    ids = [id_tuple[0] for id_tuple in _extract_ids_from_css(css_path)]
    return ids

def is_enabled(profile, theme_id):
    profile = _profile_exists(profile)
    if not check_installed(profile):
        raise RuntimeError('zen-explorer not installed')

    profile_path = _profile_path(profile)

    if not check_installed(profile):
        print('theme not installed')
        return False

    with open(f'{profile_path}/chrome/zen-explorer.json', 'r') as f:
        data = json.load(f)
        try:
            return data[theme_id]['enabled']
        except KeyError:
            pass
    if theme_id in get_enabled_themes(profile):
        return True

    return False

def is_updateable(profile, theme_id):
    profile = _profile_exists(profile)
    if not check_installed(profile):
        raise RuntimeError('not installed')

    profile_path = _profile_path(profile)

    with open(f'{profile_path}/chrome/zen-explorer.json', 'r') as f:
        data = json.load(f)

    zen_theme: Optional[theme.Theme] = repository.data.get_theme(theme_id)
    if not zen_theme:
        return False

    if zen_theme.updated_at.timestamp() > data[theme_id].get('updatedAt', 0):
        return True
    return False

def migrate_explorer_json(profile):
    profile = _profile_exists(profile)
    if not check_installed(profile):
        pass

    profile_path = _profile_path(profile)

    if not os.path.isfile(f'{profile_path}/chrome/zen-explorer.json'):
        return

    with open(f'{profile_path}/chrome/zen-explorer.json', 'r') as f:
        data = json.load(f)

    for zen_theme in data:
        data[zen_theme]['enabled'] = is_enabled(profile, zen_theme)

    with open(f'{profile_path}/chrome/zen-explorer.json', 'w+') as f:
        # noinspection PyTypeChecker
        json.dump(data, f, indent=4)

for profile in zen_profiles:
    print(f'Updating profile: {profile}')
    migrate_explorer_json(profile)

def _build_css(data):
    chrome_lines = []
    content_lines = []
    for zen_theme in data:
        try:
            if not data[zen_theme]['enabled']:
                enabled = False
            else:
                enabled = True
        except Exception:
            enabled = True
        for target in data[zen_theme]['uclChromeTarget']:
            if enabled:
                chrome_lines.append(f'@import url("zen-explorer-themes/{zen_theme}/{target}");')
        for target in data[zen_theme]['uclContentTarget']:
            try:
                if not data[zen_theme]['enabled']:
                    continue
            except KeyError:
                pass
            if enabled:
                content_lines.append(f'@import url("zen-explorer-themes/{zen_theme}/{target}");')

    return '\n'.join(chrome_lines), '\n'.join(content_lines)

def _append_to_file(path, line):
    with open(path, 'r') as f:
        lines = f.readlines()

    userchrome = [line[:-1] for line in lines if line.endswith('\n')]
    print(line, userchrome, line in userchrome)
    if line not in userchrome:
        lines.insert(0, f'{line}\n')
        with open(path, 'w+') as f:
            f.writelines(lines)

def _apply_css(path, data):
    chrome, content = _build_css(data)

    with open(f'{path}/chrome/silkthemes-chrome.css', 'w+') as f:
        f.write(chrome)

    with open(f'{path}/chrome/silkthemes-content.css', 'w+') as f:
        f.write(content)

    if os.path.isfile(f'{path}/chrome/userChrome.css'):
        shutil.copyfile(f'{path}/chrome/userChrome.css', f'{path}/chrome/userChrome.css.bak')
        _append_to_file(f'{path}/chrome/userChrome.css', '@import url("silkthemes-chrome.css");')
    else:
        with open(f'{path}/chrome/userChrome.css', 'w+') as f:
            f.write('@import url("silkthemes-chrome.css");')

    if os.path.isfile(f'{path}/chrome/userContent.css'):
        shutil.copyfile(f'{path}/chrome/userContent.css', f'{path}/chrome/userContent.css.bak')
        _append_to_file(f'{path}/chrome/userContent.css', '@import url("silkthemes-content.css");')
    else:
        with open(f'{path}/chrome/userContent.css', 'w+') as f:
            f.write('@import url("silkthemes-content.css");')

def is_installed(profile, theme_id):
    if not check_installed(profile):
        return False
    else:
        with open(f'{_profile_path(profile)}/chrome/zen-explorer.json', 'r') as f:
            data = json.load(f)
        return theme_id in data

def install_theme(profile, theme_id, bypass_install=False, staging=False, write_css=True):
    print(f'trying to install theme: {theme_id}')
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
            try:
                shutil.copy2(f'{theme_path}/{file}', f'{profile_path}/chrome/zen-explorer-themes/{theme_id}/{file}')
            except FileNotFoundError:
                print(f'File not found: {theme_path}/{file}, skipping') # TODO add handling on github or local side

                pass

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
        # Only apply CSS if write_css is True
        if write_css:
            _apply_css(profile_path, new_data)

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

def update_theme(profile, theme_id):
    install_theme(profile, theme_id, bypass_install=True, write_css=False)

def uninstall_theme(profile, theme_id, staging=False):
    profile = _profile_exists(profile)
    if not check_installed(profile):
        raise RuntimeError('not installed')

    profile_path = _profile_path(profile)

    with open(f'{profile_path}/chrome/zen-explorer.json', 'r') as f:
        data = json.load(f)

    if theme_id not in data:
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

def get_updates(profile) -> list:
    profile = _profile_exists(profile)
    if not check_installed(profile):
        raise RuntimeError('not installed')

    profile_path = _profile_path(profile)

    with open(f'{profile_path}/chrome/zen-explorer.json', 'r') as f:
        data = json.load(f)

    updates = []
    for theme_id in data:
        if is_updateable(profile, theme_id):
            updates.append(theme_id)

    return updates

def disable_theme(profile, theme_id, staging=False):
    profile = _profile_exists(profile)
    if not check_installed(profile):
        raise RuntimeError('not installed')

    profile_path = _profile_path(profile)

    with open(f'{profile_path}/chrome/zen-explorer.json', 'r') as f:
        data = json.load(f)
    print(data)
    print(theme_id)
    print(theme_id in data)
    if not is_installed(profile, theme_id):
        raise FileNotFoundError('theme not installed')

    if not is_enabled(profile, theme_id):
        print(f'Theme {theme_id} is already disabled')
        return


    if staging:
        print('Simulated data update')
    else:
        with open(f'{profile_path}/chrome/zen-explorer.json', 'w+') as f:
            # noinspection PyTypeChecker
            data[theme_id]['enabled'] = False
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

def enable_theme(profile, theme_id, staging=False):
    profile = _profile_exists(profile)
    if not check_installed(profile):
        raise RuntimeError('not installed')

    profile_path = _profile_path(profile)

    if not check_installed(profile):
        raise RuntimeError('theme not installed')

    with open(f'{profile_path}/chrome/zen-explorer.json', 'r') as f:
        data = json.load(f)

    if theme_id not in data:
        raise FileNotFoundError('theme not installed')

    data[theme_id]['enabled'] = True

    if staging:
        print('Simulated data update')
    else:
        with open(f'{profile_path}/chrome/zen-explorer.json', 'w+') as f:
            # noinspection PyTypeChecker
            data[theme_id]['enabled'] = True
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
