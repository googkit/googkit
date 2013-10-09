import os
import sys
import lib.path
import lib.plugin
from lib.command import CommandTree
from lib.config import Config
from lib.environment import Environment
from lib.error import GoogkitError


PROJECT_CONFIG = 'googkit.cfg'
USER_CONFIG = '.googkit'
DEFAULT_CONFIG = 'config/default.cfg'


def print_help(tree, args=[]):
    right_commands = tree.right_commands(args)
    if len(right_commands) == 0:
        print('Usage: googkit <command>')
    else:
        print('Usage: googkit %s <command>' % (' '.join(right_commands)))

    print('')
    print('Available commands:')

    available_commands = tree.available_commands(right_commands)
    for name in available_commands:
        print('    ' + name)


def find_config():
    default_config = lib.path.default_config()
    user_config = lib.path.user_config()
    project_config = lib.path.project_config()

    config = Config()
    config.load(project_config, user_config, default_config)
    return config


if __name__ == '__main__':
    tree = CommandTree()
    lib.plugin.load(tree)

    if len(sys.argv) < 2:
        print_help(tree)
        sys.exit()

    args = sys.argv[1:]
    classes = tree.command_classes(args)
    if classes is None:
        print_help(tree, args)
        sys.exit()

    try:
        config = None
        for cls in classes:
            if config is None and cls.needs_config():
                config = find_config()

            env = Environment(args, tree, config)
            command = cls(env)
            command.run()
    except GoogkitError as e:
        sys.exit('[ERROR] ' + str(e))
