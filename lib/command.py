from commands.apply_config import ApplyConfigCommand
from commands.commands import CommandsCommand
from commands.compile import CompileCommand
from commands.init import InitCommand
from commands.setup import SetupCommand
from commands.update_deps import UpdateDepsCommand


class CommandParser(object):
    DICT = {
        'commands': [CommandsCommand],
        'compile': [CompileCommand],
        'config': {
            'update': [ApplyConfigCommand, UpdateDepsCommand]
        },
        'deps': {
            'update': [UpdateDepsCommand]
        },
        'init': [InitCommand],
        'setup': [SetupCommand, UpdateDepsCommand],
        'update': [ApplyConfigCommand, UpdateDepsCommand]
    }

    @classmethod
    def right_commands(cls, args):
        command_dict = CommandParser.DICT
        result = []

        for arg in args:
            next_dict = command_dict.get(arg)
            if next_dict is None:
                break

            result.append(arg)
            command_dict = next_dict

        return result

    @classmethod
    def available_commands(cls, args=[]):
        command_dict = CommandParser.DICT

        for arg in args:
            next_dict = command_dict.get(arg)
            if next_dict is None:
                return []

            command_dict = next_dict

        if not isinstance(command_dict, dict):
            return []

        return command_dict.keys()


    @classmethod
    def command_classes(cls, args):
        value = CommandParser.DICT

        for arg in args:
            next_value = value.get(arg)

            if next_value is None:
                return None

            if isinstance(next_value, list):
                return next_value

            value = next_value

        return None
