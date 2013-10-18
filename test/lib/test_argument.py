import unittest
from googkit.lib.argument import ArgumentParser


class TestArgumentParser(unittest.TestCase):
    def assertListEqual(self, actual, expected, msg=None):
        if hasattr(self, 'assertItemsEqual'):
            self.assertItemsEqual(actual, expected, msg)
        else:
            self.assertCountEqual(actual, expected, msg)

    def test_parse_with_no_args(self):
        arg = ArgumentParser.parse([])
        self.assertListEqual(arg.commands, [])
        self.assertEqual(len(arg.options.keys()), 0)

    def test_parse_with_commands(self):
        arg = ArgumentParser.parse(['googkit.py', 'cmd1', 'cmd2', 'cmd3'])
        self.assertListEqual(arg.commands, ['cmd1', 'cmd2', 'cmd3'])
        self.assertEqual(len(arg.options.keys()), 0)

    def test_parse_with_key_value_option(self):
        arg = ArgumentParser.parse(['googkit.py', '--opt1=value'])
        self.assertListEqual(arg.commands, [])
        self.assertEqual(arg.option('--opt1'), 'value')

    def test_parse_with_options(self):
        arg = ArgumentParser.parse(['googkit.py', '-o', '--opt2'])
        self.assertListEqual(arg.commands, [])
        self.assertTrue(arg.option('-o'))
        self.assertTrue(arg.option('--opt2'))

    def test_parse_with_commands_and_options(self):
        arg = ArgumentParser.parse(['googkit.py', 'cmd1', '--opt1', 'cmd2', '--opt2', 'cmd3'])
        self.assertListEqual(arg.commands, ['cmd1', 'cmd2', 'cmd3'])
        self.assertTrue(arg.option('--opt1'))
        self.assertTrue(arg.option('--opt2'))
