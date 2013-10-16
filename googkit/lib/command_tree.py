from googkit.commands.build import BuildCommand
from googkit.commands.command import Command
from googkit.commands.commands import CommandsCommand
from googkit.commands.init import InitCommand
from googkit.commands.ready import ReadyCommand
from googkit.commands.setup import SetupCommand
from googkit.commands.update_deps import UpdateDepsCommand


class CommandTree(object):
    DEFAULT_TREE = {
        '_commands': [CommandsCommand],
        'build': [BuildCommand],
        'config': {
            'apply': [ReadyCommand]
        },
        'deps': {
            'update': [UpdateDepsCommand]
        },
        'init': [InitCommand],
        'ready': [ReadyCommand],
        'setup': [SetupCommand]
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

    def command_classes(self, args):
        value = self._tree
        last_value = None

        # TODO: is there a better way...?
        if len(args) > 1 and args[0] == '_commands':
            return self._tree['_commands']

        for arg in args:
            # Extra argument found after existing commands
            if last_value is not None:
                return None

            next_value = value.get(arg)

            if isinstance(next_value, dict):
                value = next_value
                continue

            if isinstance(next_value, list):
                last_value = next_value
                continue

            return None

        return last_value

    def register(self, names, commands):
        command_dict = self._tree

        for name in names[:-1]:
            command_dict[name] = {}
            command_dict = command_dict[name]

        command_dict[names[-1]] = commands
