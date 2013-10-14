import unittest

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock


from googkit.commands.commands import CommandsCommand
from googkit.commands.command import Command
from googkit.lib.argument_parser import ArgumentParser
from test.stub_environment import StubEnvironment
from test.stub_config import *


class TestCommandsCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.cmd = CommandsCommand(self.env)

    def test_init(self):
        self.assertTrue(isinstance(self.cmd, Command))

    def test_run_internal(self):
        parser = ArgumentParser()
        parser.parse(['googkit.py', 'arg1', 'arg2'])

        self.env.arg_parser = parser
        self.env.tree = mock.MagicMock()
        self.env.tree.available_commands.return_value = ['DUMMY1', 'DUMMY2']

        with mock.patch('sys.stdout', create=True) as mock_stdout:
            self.cmd.run_internal()

        mock_stdout.write.assert_any_call('DUMMY1\nDUMMY2')