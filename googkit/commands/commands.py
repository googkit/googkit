from googkit.commands.command import Command


class CommandsCommand(Command):
    def __init__(self, env):
        super(CommandsCommand, self).__init__(env)

    def complete(self):
        pass

    def run_internal(self):
        commands = self.env.arg_parser.commands[1:]
        available_commands = self.env.tree.available_commands(commands)
        print('\n'.join(available_commands))
