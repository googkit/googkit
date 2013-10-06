from command import Command
import lib.command


class CommandsCommand(Command):
    def __init__(self, env):
        super(CommandsCommand, self).__init__(env)


    def complete(self):
        pass


    def run_internal(self):
        args = self.env.args[1:]
        commands = lib.command.CommandParser.available_commands(args)
        print('\n'.join(commands))
