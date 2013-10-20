from googkit.commands.command import Command


class SequenceCommand(Command):
    """Command class that runs internal commands sequentially."""

    @classmethod
    def _internal_commands(cls):
        # Override to set internal commands
        return []

    def run(self):
        for CommandClass in self.__class__._internal_commands():
            command = CommandClass(self.env)
            command.run()
