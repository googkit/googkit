class Help(object):
    def __init__(self, tree, argument):
        self._tree = tree
        self._argument = argument
        self._correct_commands = tree.right_commands(argument.commands)
        self._available_commands = tree.available_commands(self._correct_commands)

    def _is_valid_commands(self):
        commands = self._argument.commands
        return (not commands) or (commands == self._correct_commands)

    def _print_usage(self):
        commands_mark = '<commands>' if self._available_commands else ''

        if self._correct_commands:
            print('Usage: googkit {cmd} {cmds_mark}'.format(
                cmd=' '.join(self._correct_commands),
                cmds_mark=commands_mark))
        else:
            print('Usage: googkit {cmds_mark}'.format(
                cmds_mark=commands_mark))

    def _print_available_commands(self):
        if not self._available_commands:
            return

        print('')

        if self._is_valid_commands():
            print('Available commands:')
        else:
            print('Did you mean one of these?')

        for name in self._available_commands:
            print('    ' + name)

    def print_help(self):
        if not self._is_valid_commands():
            last_command = self._argument.commands[-1]
            print('Invalid command: {cmd}'.format(cmd=last_command))
            print('')

        self._print_usage()
        self._print_available_commands()
