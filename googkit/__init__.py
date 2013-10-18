import logging
import os
import sys
import googkit.lib.path
import googkit.lib.plugin
from googkit.lib.argument_parser import ArgumentParser
from googkit.lib.command_tree import CommandTree
from googkit.lib.environment import Environment
from googkit.lib.error import GoogkitError


VERSION = '0.0.0'


def print_help(tree, commands=[]):
    """Print help.

    :param tree: `CommandTree` stored available commands.
    :param commands: Commands was given by user.

    If an empty commands was given, print an usage and availables:
        >>> from googkit.compat.unittest import mock
        >>> tree = mock.MagicMock()
        >>> tree.right_commands.return_value = []
        >>> tree.available_commands.return_value = ['sub1', 'sub2']
        ...
        >>> print_help(tree, [])
        Usage: googkit <command>
        <BLANKLINE>
        Available commands:
            sub1
            sub2

    If a branch command was given, print an usage and availables:
        >>> from googkit.compat.unittest import mock
        >>> tree = mock.MagicMock()
        >>> tree.right_commands.return_value = ['sub']
        >>> tree.available_commands.return_value = ['subsub1', 'subsub2']
        ...
        >>> print_help(tree, ['sub'])
        Usage: googkit sub <command>
        <BLANKLINE>
        Available commands:
            subsub1
            subsub2

    If an invalid command was given, print an error and expecteds:
        >>> from googkit.compat.unittest import mock
        >>> tree = mock.MagicMock()
        >>> tree.right_commands.return_value = []
        >>> tree.available_commands.return_value = ['sub1', 'sub2']
        ...
        >>> print_help(tree, ['invalid'])
        Invalid command: invalid
        <BLANKLINE>
        Did you mean one of these?
            sub1
            sub2
    """
    right_commands = tree.right_commands(commands)
    available_commands = tree.available_commands(right_commands)
    valid = not commands or commands == right_commands

    if not valid:
        print('Invalid command: {cmd}\n'.format(cmd=commands[-1]))
    elif right_commands:
        print('Usage: googkit {cmd} <command>\n'.format(cmd=' '.join(commands)))
    else:
        print('Usage: googkit <command>\n')

    if available_commands:
        if valid:
            print('Available commands:')
        else:
            print('Did you mean one of these?')

        for name in available_commands:
            print('    ' + name)


def print_version():
    print('googkit ' + VERSION)


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    tree = CommandTree()
    googkit.lib.plugin.load(tree)

    cwd = os.getcwd()

    parser = ArgumentParser()
    parser.parse(sys.argv)
    commands = parser.commands

    if len(commands) == 0 and parser.option('--version'):
        print_version()
        sys.exit()

    CommandClass = tree.command_class(commands)
    if CommandClass is None:
        print_help(tree, commands)
        sys.exit()

    try:
        env = Environment(cwd, parser, tree)
        command = CommandClass(env)
        command.run()
        logging.info('Complete.')
    except GoogkitError as e:
        logging.error('[Error] ' + str(e))
        sys.exit(1)
