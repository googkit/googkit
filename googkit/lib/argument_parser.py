import re


class ArgumentParser(object):
    OPTION_PATTERN = re.compile('(--?\w+)(?:=(.+))?')

    def __init__(self):
        self._commands = []
        self._options = {}

    def parse(self, argv):
        commands = []
        options = {}

        for arg in argv[1:]:
            if ArgumentParser._is_option(arg):
                key, value = ArgumentParser._parse_option(arg)
                options[key] = value
            else:
                commands.append(arg)

        self._commands = commands
        self._options = options

    @classmethod
    def _is_option(cls, arg):
        return ArgumentParser.OPTION_PATTERN.match(arg)

    @classmethod
    def _parse_option(cls, option):
        m = ArgumentParser.OPTION_PATTERN.match(option)
        if m is None:
            return (option, True)

        if m.lastindex == 1:
            return (m.group(1), True)

        return (m.group(1), m.group(2))

    @property
    def commands(self):
        return self._commands

    @property
    def options(self):
        return self._options

    def option(self, name):
        return self._options.get(name)
