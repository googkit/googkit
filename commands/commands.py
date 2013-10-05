import lib.command


class CommandsCommand(object):
    def __init__(self, env):
        self.env = env


    @classmethod
    def needs_config(cls):
        return False


    def run(self):
        args = self.env.args[1:]
        commands = lib.command.CommandParser.available_commands(args)
        print('\n'.join(commands))
