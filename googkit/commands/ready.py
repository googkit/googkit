import logging
from googkit.commands.apply_config import ApplyConfigCommand
from googkit.commands.sequence import SequenceCommand
from googkit.commands.update_deps import UpdateDepsCommand


class ReadyCommand(SequenceCommand):
    """Command class that gets ready for running the web app."""

    @classmethod
    def _internal_commands(cls):
        return [
            ApplyConfigCommand,
            UpdateDepsCommand
        ]
