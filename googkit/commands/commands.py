from googkit.commands.command import Command


class CommandsCommand(Command):
    """Command class that lists available subcommands for the specified arguments.
    An output will be used for shell completion.
    """

    @classmethod
    def supported_options(cls):
        return set()

    def run_internal(self):
        commands = self.env.argument.commands[1:]
        available_commands = self.env.tree.available_commands(commands)
        print('\n'.join(available_commands))
