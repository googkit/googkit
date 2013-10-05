import os
import sys
from lib.command import CommandParser
from lib.config import Config
from lib.error import GoogkitError


CONFIG = 'googkit.cfg'


def print_help(args=[]):
    commands = CommandParser.right_commands(args)
    if len(commands) == 0:
        print('Usage: googkit <command>')
    else:
        print('Usage: googkit %s <command>' % (' '.join(commands)))

    print('')
    print('Available commands:')

    commands = CommandParser.available_commands(args)
    for name in sorted(commands):
        print('    ' + name)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        sys.exit()

    args = sys.argv[1:]
    classes = CommandParser.command_classes(args)
    if classes is None:
        print_help(args)
        sys.exit()

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

    try:
        for cls in classes:
            command = cls(config)
            command.run()
    except GoogkitError, e:
        sys.exit('[ERROR] ' + str(e))
