import difflib
from googkit.lib.i18n import _


class Help(object):
    """A class that prints a help message."""

    """A threshold of a similarity ratio for command candidates"""
    CANDIDATE_RATIO_THRSHOLD = 0.5

    def __init__(self, tree, argument):
        # [todo] - Add docstirng.
        self._tree = tree
        self._argument = argument
        self._correct_commands = tree.right_commands(argument.commands)
        self._available_commands = tree.available_commands(self._correct_commands)

    def _is_valid_commands(self):
        commands = self._argument.commands
        return (not commands) or (commands == self._correct_commands)

    def _print_usage(self):
        commands_mark = _('<commands>') if self._available_commands else ''

        if self._correct_commands:
            print(_('Usage: googkit {cmd} {cmds_mark}').format(
                cmd=' '.join(self._correct_commands),
                cmds_mark=commands_mark))
        else:
            print(_('Usage: googkit {cmds_mark}').format(
                cmds_mark=commands_mark))

    @classmethod
    def similarity(cls, src_command):
        """Returns a function that returns a similarity ratio for the specified
        command.
        """
        def ratio(command):
            return difflib.SequenceMatcher(None, src_command, command).ratio()
        return ratio

    @classmethod
    def candidates(cls, available_commands, src_command):
        """Returns command candidates for the specified available commands and
        the source command.
        """
        if src_command is None:
            return available_commands

        ratio = Help.similarity(src_command)
        candidates = sorted(available_commands, key=ratio, reverse=True)
        return [x for x in candidates if ratio(x) >= Help.CANDIDATE_RATIO_THRSHOLD]

    def _print_available_commands(self, command):
        if not self._available_commands:
            return

        print('')

        if self._is_valid_commands():
            print(_('Available commands:'))
            commands = self._available_commands
        else:
            candidates = Help.candidates(self._available_commands, command)
            if len(candidates) == 0:
                print(_('Available commands:'))
                commands = self._available_commands
            elif len(candidates) == 1:
                print(_('Did you mean this?'))
                commands = candidates
            else:
                print(_('Did you mean one of these?'))
                commands = candidates

        for name in commands:
            print('    ' + name)

    def _print_available_options(self):
        cls = self._tree.command_class(self._argument.commands)
        if not cls:
            return

        supported_options = cls.supported_options()
        if not supported_options:
            return

        print('')
        print(_('Available options:'))

        for name in supported_options:
            print('    ' + name)

    def print_help(self):
        # [todo] - Add docstirng.
        last_command = None if not self._argument.commands else self._argument.commands[-1]

        if not self._is_valid_commands():
            print(_('Invalid command: {cmd}').format(cmd=last_command))
            print('')

        self._print_usage()
        self._print_available_commands(last_command)
        self._print_available_options()
