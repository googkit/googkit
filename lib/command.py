from commands.apply_config import ApplyConfigCommand
from commands.compile import CompileCommand
from commands.init import InitCommand
from commands.setup import SetupCommand
from commands.update_deps import UpdateDepsCommand


class CommandParser(object):
    DICT = {
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
        dict = CommandParser.DICT
        result = []

        for arg in args:
            next_dict = dict.get(arg)
            if next_dict is None:
                break

            result.append(arg)
            dict = next_dict

        return result

    @classmethod
    def available_commands(cls, args):
        dict = CommandParser.DICT

        for arg in args:
            next_dict = dict.get(arg)
            if next_dict is None:
                return dict.keys()

            dict = next_dict

        return dict

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
