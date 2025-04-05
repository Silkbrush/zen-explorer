import sys
from zen_explorer_core import profiles, repository, installer
from zen_explorer_core.models import theme

zen_profiles = profiles.get_profiles()

def get_profiles(_args):
    global zen_profiles
    if not zen_profiles:
        print('No profiles available.')
        return

    print('Available profiles:')

    for profile in zen_profiles:
        profile_id, profile_name = profile.split('.', 1)
        print(f'{profile_name} ({profile_id})')

def update_repository(args):
    print('Updating repository...')

    try:
        if len(args) > 0:
            repository.update_repository(args[0])
        else:
            repository.update_repository()
    except:
        print('Failed to update repository.')
        raise

    print('Repository updated.')

def themes(args):
    page = 0
    if len(args) > 0:
        try:
            page = int(args[0])
        except:
            pass
    if not repository.data or not repository.data.themes:
        print('No themes available.')
        return

    maxpage = len(repository.data.themes) // 20
    if page > maxpage:
        page = maxpage

    print('Available themes')
    theme_names = list(repository.data.themes.keys())
    for x in range(page * 20, min((page + 1) * 20, len(theme_names))):
        if x >= len(theme_names):
            break
        zen_theme: theme.Theme = repository.data.get_theme(theme_names[x])
        print(f'({zen_theme.type_name} - {theme_names[x]}) {zen_theme.name} by {zen_theme.author}')

    print(f'\nPage {page + 1} of {maxpage + 1}')

def install(args):
    zen_theme = args[0]
    profile = args[1]
    staging = '--staging' in args # or True # TODO: debug, remove the "or True"
    bypass_install = '--bypass-install' in args

    if not repository.data or not repository.data.themes:
        print('No themes available.')
        return

    theme_data = repository.data.get_theme(zen_theme)
    if not theme_data:
        print('Theme not found.')
        return

    print(f'Installing {theme_data.name} by {theme_data.author}...')
    try:
        installer.install_theme(profile, zen_theme, bypass_install=bypass_install, staging=staging)
    except:
        print('Failed to install theme.')
        raise
    print('Theme installed.')

def uninstall(args):
    zen_theme = args[0]
    profile = args[1]
    staging = '--staging' in args # or True # TODO: debug, remove the "or True"

    print('Uninstalling theme...')
    try:
        installer.uninstall_theme(profile, zen_theme, staging=staging)
    except:
        print('Failed to uninstall theme.')
        raise
    print('Theme uninstalled.')

def upgrade(args):
    profile = args[0]
    print('Checking for updates...')

    try:
        updates = installer.get_updates(profile)
    except:
        print('Failed to check for updates.')
        raise

    if not updates:
        print('No updates available.')
        return

    print('Available updates:')
    for zen_theme in updates:
        print(f'{updates[zen_theme].name} ({updates[zen_theme].version})')

    choice = input('\nUpdate themes? (Y/n): ')
    if choice.lower() != 'y':
        return

    print('Updating themes...')
    for zen_theme in updates:
        try:
            installer.install_theme(profile, zen_theme, bypass_install=True)
        except:
            print(f'Failed to update {updates[zen_theme].name}.')
            raise

    print('Themes updated.')

def cli_help(_args):
    print('Zen Explorer CLI Help')
    for command in command_mappings:
        print(f'{command} - {command_mappings[command].get("description", "no description")}')

def main():
    args = list(sys.argv)
    args.pop(0)

    if len(args) == 0:
        command = 'help'
    else:
        command = args[0]

    command_args = args[1:]

    if command in command_mappings.keys():
        command_mappings[command]['func'](command_args)
    else:
        print(f'Unknown command: {command}')


command_mappings = {
    'help': {
        'description': 'Shows a list of all commands.',
        'func': cli_help
    },
    'profiles': {
        'description': 'Gets a list of profiles.',
        'func': get_profiles
    },
    'update': {
        'description': 'Updates themes repository.',
        'func': update_repository
    },
    'themes': {
        'description': 'Lists available themes.',
        'func': themes
    },
    'install': {
        'description': 'Installs a theme.',
        'func': install
    },
    'uninstall': {
        'description': 'Uninstalls a theme.',
        'func': uninstall
    },
    'upgrade': {
        'description': 'Updates installed themes.',
        'func': upgrade
    }
}

# Run CLI if invoked directly
# Otherwise, CLI functions can be used for the sake of abstraction
if __name__ == '__main__':
    main()
