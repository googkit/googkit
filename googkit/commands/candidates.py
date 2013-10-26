from googkit.commands.command import Command
from googkit.lib.argument import ArgumentParser


class CandidatesCommand(Command):
    """Command class that lists available subcommands and options
    for the specified arguments.
    An output will be used for shell completion.
    """

    def _internal_argument(self):
        # ArgumentParser ignores the first argument because it's a script name.
        # So parse(commands) ignores the first command `_candidates`
        # and should work fine.
        return ArgumentParser.parse(self.env.argument.commands)

    def _command_candidates(self):
        arg = self._internal_argument()
        return self.env.tree.available_commands(arg.commands)

    def _option_candidates(self):
        arg = self._internal_argument()
        CommandClass = self.env.tree.command_class(arg.commands)
        if CommandClass is None:
            return []

        supported_opts = CommandClass.supported_options()
        specified_opts = set(self.env.argument.options.keys())

        return list(supported_opts - specified_opts)

    def run(self):
        # Call run_internal directly and skip option validation
        # because it should accept all options for completion.
        self.run_internal()

    def run_internal(self):
        candidates = self._command_candidates() + self._option_candidates()
        print('\n'.join(candidates))
