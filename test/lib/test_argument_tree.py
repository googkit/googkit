import unittest
from googkit.lib.argument_parser import ArgumentParser


class TestArgumentParser(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

    def assertListEqual(self, actual, expected, msg=None):
        if hasattr(self, 'assertItemsEqual'):
            self.assertItemsEqual(actual, expected, msg)
        else:
            self.assertCountEqual(actual, expected, msg)

    def test_parse_with_no_args(self):
        self.parser.parse([])
        self.assertListEqual(self.parser.commands, [])
        self.assertEqual(len(self.parser.options.keys()), 0)

    def test_parse_with_commands(self):
        self.parser.parse(['googkit.py', 'cmd1', 'cmd2', 'cmd3'])
        self.assertListEqual(self.parser.commands, ['cmd1', 'cmd2', 'cmd3'])
        self.assertEqual(len(self.parser.options.keys()), 0)

    def test_parse_with_key_value_option(self):
        self.parser.parse(['googkit.py', '--opt1=value'])
        self.assertListEqual(self.parser.commands, [])
        self.assertEqual(self.parser.option('--opt1'), 'value')

    def test_parse_with_options(self):
        self.parser.parse(['googkit.py', '-o', '--opt2'])
        self.assertListEqual(self.parser.commands, [])
        self.assertTrue(self.parser.option('-o'))
        self.assertTrue(self.parser.option('--opt2'))

    def test_parse_with_commands_and_options(self):
        self.parser.parse(['googkit.py', 'cmd1', '--opt1', 'cmd2', '--opt2', 'cmd3'])
        self.assertListEqual(self.parser.commands, ['cmd1', 'cmd2', 'cmd3'])
        self.assertTrue(self.parser.option('--opt1'))
        self.assertTrue(self.parser.option('--opt2'))
