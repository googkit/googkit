import unittest

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock

from googkit.commands.command import Command
from googkit.commands.sequence import SequenceCommand

from test.stub_environment import StubEnvironment


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

        with mock.patch('test.commands.test_sequence.DummyFooCommand') as mock_foo, \
                mock.patch('test.commands.test_sequence.DummyBarCommand') as mock_bar:
            command.run()

        mock_foo.run.assert_called_once()
        mock_bar.run.assert_called_once()
        # TODO: Is it possible to test an execution order of those commands?
