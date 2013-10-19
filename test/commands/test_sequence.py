import unittest

from test.stub_environment import StubEnvironment

from googkit.commands.command import Command
from googkit.commands.sequence import SequenceCommand
from googkit.compat.unittest import mock


class DummyFooCommand(Command):
    pass


class DummyBarCommand(Command):
    pass


class TestSequenceCommand(unittest.TestCase):
    def test_run(self):
        class DummySequenceCommand(SequenceCommand):
            @classmethod
            def _internal_commands(cls):
                return [
                    DummyFooCommand,
                    DummyBarCommand
                ]

        env = StubEnvironment()
        command = DummySequenceCommand(env)

        with mock.patch('test.commands.test_sequence.DummyFooCommand') as MockFoo, \
                mock.patch('test.commands.test_sequence.DummyBarCommand') as MockBar:
            command.run()

        self.assertTrue(MockFoo.return_value.run.called)
        self.assertTrue(MockBar.return_value.run.called)
        # TODO: Is it possible to test an execution order of those commands?
