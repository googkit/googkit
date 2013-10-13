import logging
import os
import sys
import googkit.lib.path
import googkit.lib.plugin
from googkit.lib.command_tree import CommandTree
from googkit.lib.config import Config
from googkit.lib.environment import Environment
from googkit.lib.error import GoogkitError


GOOGKIT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_CONFIG = 'googkit.cfg'
USER_CONFIG = '.googkit'
DEFAULT_CONFIG = os.path.join(GOOGKIT_ROOT, 'config', 'default.cfg')


def print_help(tree, args=[]):
    right_commands = tree.right_commands(args)
    if len(right_commands) == 0:
        print('Usage: googkit <command>')
    else:
        print('Usage: googkit {cmd} <command>'.format(cmd=' '.join(right_commands)))

    print('')
    print('Available commands:')

    available_commands = tree.available_commands(right_commands)
    for name in available_commands:
        print('    ' + name)


def find_config():
    default_config = googkit.lib.path.default_config()
    user_config = googkit.lib.path.user_config()
    project_config = googkit.lib.path.project_config()
    config = Config()
    config.load(project_config, user_config, default_config)
    return config


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    tree = CommandTree()
    googkit.lib.plugin.load(tree)

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
                os.chdir(googkit.lib.path.project_root())
                config = find_config()

            env = Environment(args, tree, config)
            command = cls(env)
            command.run()
    except GoogkitError as e:
        logging.error('[Error] ' + str(e))
        sys.exit(1)
