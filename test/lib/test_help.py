import unittest

from test.stub_stdout import StubStdout

from googkit.compat.unittest import mock
from googkit.lib.command_tree import CommandTree
from googkit.lib.argument import ArgumentParser
from googkit.lib.help import Help


class TestHelp(unittest.TestCase):
    def setUp(self):
        CommandTree.DEFAULT_TREE = {
            '0_leaf': mock.MagicMock(),
            '0_node': {
                '1_leaf': mock.MagicMock(),
                '1_node': {
                    '2_leaf': mock.MagicMock()
                }
            }
        }
        self.tree = CommandTree()

    def help_with_args(self, args):
        arg = ArgumentParser.parse(['googkit.py'] + args)
        return Help(self.tree, arg)

    def test_is_valid_commands(self):
        help = self.help_with_args(['0_leaf'])
        self.assertTrue(help._is_valid_commands())

        help = self.help_with_args(['0_node', '1_leaf'])
        self.assertTrue(help._is_valid_commands())

        help = self.help_with_args(['0_node', '1_leaf', 'bluerose'])
        self.assertFalse(help._is_valid_commands())

    def test_print_usage(self):
        help = self.help_with_args(['0_leaf'])
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            help._print_usage()
        self.assertFalse(mock_stdout.getvalue().find('<commands>') >= 0)

        help = self.help_with_args(['bluerose'])
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            help._print_usage()
        self.assertTrue(mock_stdout.getvalue().find('<commands>') >= 0)

        help = self.help_with_args(['0_leaf', 'bluerose'])
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            help._print_usage()
        self.assertFalse(mock_stdout.getvalue().find('<commands>') >= 0)

        help = self.help_with_args(['0_node'])
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            help._print_usage()
        self.assertTrue(mock_stdout.getvalue().find('<commands>') >= 0)

    def test_print_available_commands(self):
        help = self.help_with_args(['0_leaf'])
        with mock.patch('sys.stdout') as mock_stdout:
            help._print_available_commands()
        self.assertFalse(mock_stdout.write.called)

        help = self.help_with_args(['0_node'])
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            help._print_available_commands()
        self.assertTrue(mock_stdout.getvalue().find('Available commands') >= 0)

        help = self.help_with_args(['0_node', 'bluerose'])
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            help._print_available_commands()
        self.assertTrue(mock_stdout.getvalue().find('Did you mean one of these') >= 0)

    def test_print_help(self):
        help = self.help_with_args(['0_leaf'])
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            help.print_help()
        self.assertFalse(mock_stdout.getvalue().find('Invalid command') >= 0)

        help = self.help_with_args(['0_leaf', 'bluerose'])
        with mock.patch('sys.stdout', new_callable=StubStdout) as mock_stdout:
            help.print_help()
        self.assertTrue(mock_stdout.getvalue().find('Invalid command') >= 0)
