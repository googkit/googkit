import logging
import os
import sys
import googkit.lib.path
import googkit.lib.plugin
from googkit.lib.argument import ArgumentParser
from googkit.lib.command_tree import CommandTree
from googkit.lib.environment import Environment
from googkit.lib.error import GoogkitError
from googkit.lib.error import InvalidOptionError
from googkit.lib.help import Help


VERSION = '0.1.2'


def print_version():
    print('googkit ' + VERSION)


def main():
    cwd = os.getcwd()
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    tree = CommandTree()
    googkit.lib.plugin.load(tree)

    arg = ArgumentParser.parse(sys.argv)

    if not arg.commands and arg.option('--version'):
        print_version()
        sys.exit()

    CommandClass = tree.command_class(arg.commands)
    if CommandClass is None:
        Help(tree, arg).print_help()
        sys.exit()

    try:
        env = Environment(cwd, arg, tree)
        command = CommandClass(env)
        command.run()
    except InvalidOptionError as e:
        logging.error('[Error] ' + str(e))
        Help(tree, arg).print_help()
        sys.exit(1)
    except GoogkitError as e:
        logging.error('[Error] ' + str(e))
        sys.exit(1)
