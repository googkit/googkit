from googkit.commands.command import Command


class CommandsCommand(Command):
    """
    Command class that lists available subcommands for the specified arguments.
    An output will be used for shell completion.
    """

    def __init__(self, env):
        super(CommandsCommand, self).__init__(env)

    def complete(self):
        pass

    def run_internal(self):
        commands = self.env.arg_parser.commands[1:]
        available_commands = self.env.tree.available_commands(commands)
        print('\n'.join(available_commands))
