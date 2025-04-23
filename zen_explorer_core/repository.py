import os
import json
import shutil
import platformdirs
from typing import Optional
from zen_explorer_core.models import theme

save_dir = os.environ.get('WORKING_DIR') or platformdirs.user_data_dir('zen-explorer')

class RepositoryData:
    def __init__(self, path, data):
        self._path = path
        self._raw_data = data
        self._themes = {}

        for zen_theme in self._raw_data:
            if not os.path.isfile(f'{self._path}/themes/{zen_theme}/theme.json'):
                continue
            with open(f'{self._path}/themes/{zen_theme}/theme.json') as f:
                install_data = json.load(f)
            self._themes[zen_theme] = theme.Theme(self._raw_data[zen_theme], install_data=install_data, _id=zen_theme)

    @property
    def path(self):
        return self._path

    @property
    def themes(self):
        return self._themes

    def get_theme(self, zen_theme) -> Optional[theme.Theme]:
        return self._themes.get(zen_theme)

    def get_theme_readme(self, zen_theme) -> Optional[str]:
        if not zen_theme in self._themes:
            return None
        with open(f'{self._path}/themes/{zen_theme}/README.md') as f:
            readme = f.read()
        return readme

def repository_path():
    if not os.path.isdir(f'{save_dir}/repository'):
        raise NotADirectoryError('repository not available, run update_repository')

    return f'{save_dir}/repository'

def update_repository(repo: str = 'greeeen-dev/zen-custom-theme-store'):
    global data

    if os.path.isdir(save_dir + '/repository'):
        code = os.system(f'cd "{save_dir}/repository" && git pull --quiet')
    else:
        code = os.system(f'git clone https://github.com/{repo} "{save_dir}/repository" --quiet')
    if code != 0:
        raise RuntimeError('failed to update')

    with open(f'{save_dir}/repository/themes.json') as f:
        themes = json.load(f)

    data = RepositoryData(f'{save_dir}/repository', themes)

def delete_repository():
    if os.path.isdir(save_dir + '/repository'):
        shutil.rmtree(f'{save_dir}/repository')
    else:
        raise NotADirectoryError('repository not found')


data: RepositoryData | None = None
if os.path.isfile(save_dir + '/repository/themes.json'):
    with open(f'{save_dir}/repository/themes.json') as f:
        themes = json.load(f)

    data = RepositoryData(f'{save_dir}/repository', themes)
else:
    print('themes.json not found in repository directory')
