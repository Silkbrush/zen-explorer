import os
import platformdirs

save_dir = os.environ.get('WORKING_DIR') or platformdirs.user_data_dir('zen-explorer')

def update_repository(repo: str = 'greeeen-dev/zen-custom-theme-store'):
    if os.path.isdir(save_dir + '/repository'):
        code = os.system(f'cd "{save_dir}/repository" && git pull')
    else:
        code = os.system(f'git clone https://github.com/{repo} "{save_dir}/repository"')
    if code != 0:
        raise RuntimeError('failed to update')

def delete_repository():
    if os.path.isdir(save_dir + '/repository'):
        os.system(f'rm -rf "{save_dir}/repository"')
    else:
        raise FileNotFoundError('repository not found')
