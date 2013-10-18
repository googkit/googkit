import unittest

from test.stub_config import *
from test.stub_environment import StubEnvironment

from googkit.commands.commands import CommandsCommand
from googkit.commands.command import Command
from googkit.compat.unittest import mock
from googkit.lib.argument import ArgumentParser


class TestCommandsCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.cmd = CommandsCommand(self.env)

    def test_init(self):
        self.assertTrue(isinstance(self.cmd, Command))

    def test_run_internal(self):
        self.env.argument = ArgumentParser.parse(['googkit.py', 'arg1', 'arg2'])
        self.env.tree = mock.MagicMock()
        self.env.tree.available_commands.return_value = ['DUMMY1', 'DUMMY2']

        with mock.patch('sys.stdout', create=True) as mock_stdout:
            self.cmd.run_internal()

        mock_stdout.write.assert_any_call('DUMMY1\nDUMMY2')
