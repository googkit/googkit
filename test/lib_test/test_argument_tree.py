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
        self.assertListEqual(self.parser.options, [])

    def test_parse_with_commands(self):
        self.parser.parse(['googkit.py', 'cmd1', 'cmd2', 'cmd3'])
        self.assertListEqual(self.parser.commands, ['cmd1', 'cmd2', 'cmd3'])
        self.assertListEqual(self.parser.options, [])

    def test_parse_with_key_value_option(self):
        self.parser.parse(['googkit.py', '--opt1=value'])
        self.assertListEqual(self.parser.commands, [])
        self.assertListEqual(self.parser.options, ['--opt1=value'])

    def test_parse_with_options(self):
        self.parser.parse(['googkit.py', '--opt1', '--opt2', '--opt3'])
        self.assertListEqual(self.parser.commands, [])
        self.assertListEqual(self.parser.options, ['--opt1', '--opt2', '--opt3'])

    def test_parse_with_commands_and_options(self):
        self.parser.parse(['googkit.py', 'cmd1', '--opt1', 'cmd2', '--opt2', 'cmd3'])
        self.assertListEqual(self.parser.commands, ['cmd1', 'cmd2', 'cmd3'])
        self.assertListEqual(self.parser.options, ['--opt1', '--opt2'])
