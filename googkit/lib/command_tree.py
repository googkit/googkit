from googkit.commands.build import BuildCommand
from googkit.commands.commands import CommandsCommand
from googkit.commands.init import InitCommand
from googkit.commands.ready import ReadyCommand
from googkit.commands.setup import SetupCommand
from googkit.commands.update_deps import UpdateDepsCommand


class CommandTree(object):
    DEFAULT_TREE = {
        '_commands': CommandsCommand,
        'build': BuildCommand,
        'config': {
            'apply': ReadyCommand
        },
        'deps': {
            'update': UpdateDepsCommand
        },
        'init': InitCommand,
        'ready': ReadyCommand,
        'setup': SetupCommand
    }

    def __init__(self):
        self._tree = CommandTree.DEFAULT_TREE.copy()

    def right_commands(self, args):
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
        return name[0] == '_'

    def available_commands(self, args=[]):
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
        value = self._tree

        # TODO: is there a better way...?
        if len(args) > 1 and args[0] == '_commands':
            return self._tree['_commands']

        depth = 0
        for arg in args:
            next_value = value.get(arg)
            depth += 1

            if not isinstance(next_value, dict):
                if depth != len(args):
                    # Extra argument found after existing commands
                    # TODO: should raise an error?
                    return None

                return next_value

            value = next_value

        return None

    def register(self, names, commands):
        command_dict = self._tree

        for name in names[:-1]:
            command_dict[name] = {}
            command_dict = command_dict[name]

        command_dict[names[-1]] = commands
