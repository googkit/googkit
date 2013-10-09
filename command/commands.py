from command.base_command import BaseCommand

class CommandsCommand(BaseCommand):
    def __init__(self, env):
        super(CommandsCommand, self).__init__(env)


    def complete(self):
        pass


    def run_internal(self):
        from lib.command_parser import CommandParser
        args = self.env.args[1:]
        commands = self.env.tree.available_commands(args)
        print('\n'.join(commands))
