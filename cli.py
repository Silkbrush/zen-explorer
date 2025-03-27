import sys
from zen_explorer_core import profiles, repository

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
    }
}

if __name__ == '__main__':
    main()
