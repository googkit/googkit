from googkit.commands.build import BuildCommand
from googkit.commands.candidates import CandidatesCommand
from googkit.commands.init import InitCommand
from googkit.commands.lint import LintCommand
from googkit.commands.ready import ReadyCommand
from googkit.commands.setup import SetupCommand
from googkit.commands.update_deps import UpdateDepsCommand


class CommandTree(object):
    """A class for command tree that provides a sub-command mechanism.
    """

    """Default command tree.
    """
    DEFAULT_TREE = {
        '_candidates': CandidatesCommand,
        'build': BuildCommand,
        'config': {
            'apply': ReadyCommand
        },
        'deps': {
            'update': UpdateDepsCommand
        },
        'init': InitCommand,
        'lint': LintCommand,
        'ready': ReadyCommand,
        'setup': SetupCommand,
    }

    def __init__(self, tree=None):
        """Creates a command tree.
        You can set customized command tree by first argument.
        """
        if tree is None:
            self._tree = CommandTree.DEFAULT_TREE.copy()
        else:
            self._tree = tree

    def right_commands(self, args):
        """Returns a valid command part of the specified arguments.

        Usage::
            >>> from googkit.commands.command import Command
            >>> stub_cmd_tree = {
            ...     'sub_cmd': {'sub_sub_cmd': Command}
            ...     }
            >>> cmd_tree = CommandTree(stub_cmd_tree)
            >>> cmd_tree.right_commands(['sub_cmd', 'sub_sub_cmd', 'invalid'])
            ['sub_cmd', 'sub_sub_cmd']
        """
        command_dict = self._tree
        result = []

        for arg in args:
            next_dict = command_dict.get(arg)
            if next_dict is None:
                break

            result.append(arg)

            if not isinstance(next_dict, dict):
                break

            command_dict = next_dict

        return result

    @classmethod
    def is_internal_command(cls, name):
        """Whether the specified command is an internal command.
        """
        return name[0] == '_'

    def available_commands(self, args=[]):
        """Returns available command list.
        Optionally you can set a sub command tree to search.

        Usage::
            >>> from googkit.commands.command import Command
            >>> stub_cmd_tree = {
            ...     'sub_cmd': {
            ...         'sub_sub_cmd1': Command,
            ...         'sub_sub_cmd2': Command,
            ...         }
            ...     }
            >>> cmd_tree = CommandTree(stub_cmd_tree)
            >>> cmd_tree.available_commands()
            ['sub_sub_cmd1', 'sub_sub_cmd2']
        """
        command_dict = self._tree

        for arg in args:
            next_dict = command_dict.get(arg)
            if next_dict is None:
                return []

            command_dict = next_dict

        if not isinstance(command_dict, dict):
            return []

        commands = command_dict.keys()
        return sorted([cmd for cmd in commands if not CommandTree.is_internal_command(cmd)])

    def command_class(self, args):
        """Returns a command class by the arguments.

        Usage::
            >>> from googkit.commands.command import Command
            >>> stub_cmd_tree = {
            ...     'sub_cmd': {'sub_sub_cmd': Command}
            ...     }
            >>> cmd_tree = CommandTree(stub_cmd_tree)
            >>> cmd_tree.command_class(['sub_cmd', 'sub_sub_cmd'])
            Command
        """
        value = self._tree

        # [REVIEW] - is there a better way...?
        if len(args) > 1 and args[0] == '_candidates':
            return self._tree['_candidates']

        depth = 0
        for arg in args:
            next_value = value.get(arg)
            depth += 1

            if not isinstance(next_value, dict):
                if depth != len(args):
                    # Extra argument found after existing commands
                    # [review] - should raise an error?
                    return None

                return next_value

            value = next_value

        return None

    def register(self, names, commands):
        """Registers a commands by each name.

        Usage::
            >>> from googkit.commands.command import Command
            >>> cmd_tree = CommandTree()
            >>> cmd_tree.register(['my_cmd1', 'my_cmd2'], [Command, Command])
        """
        command_dict = self._tree

        for name in names[:-1]:
            command_dict[name] = {}
            command_dict = command_dict[name]

        command_dict[names[-1]] = commands
