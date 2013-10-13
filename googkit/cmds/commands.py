from googkit.cmds.command import Command


class CommandsCommand(Command):
    def __init__(self, env):
        super(CommandsCommand, self).__init__(env)


    def complete(self):
        pass


    def run_internal(self):
        args = self.env.args[1:]
        commands = self.env.tree.available_commands(args)
        print('\n'.join(commands))
