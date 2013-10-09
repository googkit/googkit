from commands.apply_config import ApplyConfigCommand
from commands.build import BuildCommand
from commands.commands import CommandsCommand
from commands.init import InitCommand
from commands.setup import SetupCommand
from commands.update_deps import UpdateDepsCommand


class CommandTree(object):
    DEFAULT_TREE = {
        '_commands': [CommandsCommand],
        'build': [BuildCommand],
        'config': {
            'apply': [ApplyConfigCommand, UpdateDepsCommand]
        },
        'deps': {
            'update': [UpdateDepsCommand]
        },
        'init': [InitCommand],
        'ready': [ApplyConfigCommand, UpdateDepsCommand],
        'setup': [SetupCommand, UpdateDepsCommand]
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

        for arg in args:
            next_value = value.get(arg)

            if next_value is None:
                return None

            if isinstance(next_value, list):
                return next_value

            value = next_value

        return None


    def register(self, names, commands):
        command_dict = self._tree

        for name in names[:-1]:
            command_dict[name] = {}
            command_dict = command_dict[name]

        command_dict[names[-1]] = commands
