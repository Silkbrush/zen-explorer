import json
import os
import sys
from pathlib import Path
from typing_extensions import Optional, Union, Literal
from .browser import _get_paths

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
