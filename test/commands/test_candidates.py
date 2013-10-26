import unittest

from test.stub_config import *
from test.stub_environment import StubEnvironment
from test.stub_stdout import StubStdout

from googkit.commands.candidates import CandidatesCommand
from googkit.commands.command import Command
from googkit.compat.unittest import mock
from googkit.lib.argument import ArgumentParser
from googkit.lib.command_tree import CommandTree


class TestCandidatesCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.env.tree = CommandTree()
        self.cmd = CandidatesCommand(self.env)

    def test_init(self):
        self.assertTrue(isinstance(self.cmd, Command))

    def _arg(self, arg_text):
        return ArgumentParser.parse(arg_text.split(' '))

    def test_run_internal(self):
        self.env.argument = self._arg('googkit.py _candidates deps')
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            self.cmd.run_internal()
        candidates = mock_stdout.getvalue().split('\n')
        self.assertFalse('deps' in candidates)
        self.assertTrue('update' in candidates)
        self.assertFalse('--verbose' in candidates)

        self.env.argument = self._arg('googkit.py _candidates deps update')
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            self.cmd.run_internal()
        candidates = mock_stdout.getvalue().split('\n')
        self.assertFalse('deps' in candidates)
        self.assertFalse('update' in candidates)
        self.assertTrue('--verbose' in candidates)

        self.env.argument = self._arg('googkit.py _candidates deps update --verbose')
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            self.cmd.run_internal()
        candidates = mock_stdout.getvalue().split('\n')
        self.assertFalse('deps' in candidates)
        self.assertFalse('update' in candidates)
        self.assertFalse('--verbose' in candidates)
