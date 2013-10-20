from googkit.commands.download import DownloadCommand
from googkit.commands.sequence import SequenceCommand
from googkit.commands.update_deps import UpdateDepsCommand


class SetupCommand(SequenceCommand):
    """Command class that sets up Closure Tools."""

    @classmethod
    def _internal_commands(cls):
        return [
            DownloadCommand,
            UpdateDepsCommand
        ]
