import unittest

from test.stub_stdout import StubStdout

from googkit.compat.unittest import mock
from googkit.lib.command_tree import CommandTree
from googkit.lib.argument import ArgumentParser
from googkit.lib.help import Help


class TestHelp(unittest.TestCase):
    def setUp(self):
        CommandTree.DEFAULT_TREE = {
            'a': mock.MagicMock(),
            'b': {
                'c': mock.MagicMock(),
                'd': {
                    'e': mock.MagicMock()
                }
            }
        }
        self.tree = CommandTree()

    def test_is_valid_commands(self):
        arg = ArgumentParser.parse(['googkit.py', 'a'])
        help = Help(self.tree, arg)
        self.assertTrue(help._is_valid_commands())

        arg = ArgumentParser.parse(['googkit.py', 'b', 'c'])
        help = Help(self.tree, arg)
        self.assertTrue(help._is_valid_commands())

        arg = ArgumentParser.parse(['googkit.py', 'b', 'c', 'foobar'])
        help = Help(self.tree, arg)
        self.assertFalse(help._is_valid_commands())

    def test_print_usage(self):
        arg = ArgumentParser.parse(['googkit.py', 'a'])
        help = Help(self.tree, arg)

        with mock.patch('sys.stdout', new_callable=StubStdout):
            help._print_usage()

        # TODO: Test stdout content

    def test_print_available_commands(self):
        # TODO: Test
        pass

    def test_print_help(self):
        # TODO: Test
        pass
