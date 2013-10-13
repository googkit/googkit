class ArgumentParser(object):
    def __init__(self):
        self._commands = []
        self._options = []

    def parse(self, argv):
        commands = []
        options = []

        for arg in argv[1:]:
            if arg[0] == '-':
                options.append(arg)
            else:
                commands.append(arg)

        self._commands = commands
        self._options = options

    @property
    def commands(self):
        return self._commands

    @property
    def options(self):
        return self._options
