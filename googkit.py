import os
import sys
from lib.command import CommandParser
from lib.config import Config
from lib.environment import Environment
from lib.error import GoogkitError


CONFIG = 'googkit.cfg'


def print_help(args=[]):
    right_commands = CommandParser.right_commands(args)
    if len(right_commands) == 0:
        print('Usage: googkit <command>')
    else:
        print('Usage: googkit %s <command>' % (' '.join(right_commands)))

    print('')
    print('Available commands:')

    available_commands = CommandParser.available_commands(right_commands)
    for name in available_commands:
        print('    ' + name)


def find_config():
    config = Config()
    try:
        while not os.path.exists(os.path.relpath(CONFIG)):
            before = os.getcwd()
            os.chdir('..')

            # Break if current dir is root.
            if before == os.getcwd():
                break

        config.load(CONFIG)
    except IOError:
        config = None

    return config


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        sys.exit()

    args = sys.argv[1:]
    classes = CommandParser.command_classes(args)
    if classes is None:
        print_help(args)
        sys.exit()

    try:
        config = None
        for cls in classes:
            if config is None and cls.needs_config():
                config = find_config()

            env = Environment(args, config)
            command = cls(env)
            command.run()
    except GoogkitError, e:
        sys.exit('[ERROR] ' + str(e))
