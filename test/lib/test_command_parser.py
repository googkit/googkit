# Run the following command to test:
#
#     (in /usr/local/googkit)
#     $ python -m {test_module_name}
#
# See also: http://docs.python.org/3.3/library/unittest.html#command-line-interfacejjkkjj
#
# We cannot use unittest.mock on python 2.x!
# Please install the Mock module when you use Python 2.x.
#
#     $ easy_install -U Mock
#
# See also: http://www.voidspace.org.uk/python/mock/#installing

import unittest

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock

from lib.command_parser import CommandParser



class TestCommandParser(unittest.TestCase):
    def setUp(self):
        TestCommandParser.cmd0 = mock.MagicMock()
        TestCommandParser.cmd1 = mock.MagicMock()
        TestCommandParser.cmd3 = mock.MagicMock()
        TestCommandParser.cmd5 = mock.MagicMock()

        CommandParser.DICT = {
            '_cmd0': [TestCommandParser.cmd0],
            'cmd1': [TestCommandParser.cmd1],
            'cmd2': {
                'cmd3': [TestCommandParser.cmd3],
                'cmd4': {
                    'cmd5': [TestCommandParser.cmd5]
                }
            }
        }


    # right {{{
    def test_right_commands_with_no_cmd(self):
        result = CommandParser.right_commands([])
        self.assertEqual(len(result), 0)


    def test_right_commands_with_garbage(self):
        result = CommandParser.right_commands(['cmd99'])
        self.assertEqual(len(result), 0)


    def test_right_commands_with_main_cmd(self):
        result = CommandParser.right_commands(['cmd1'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd1')


    def test_right_commands_with_main_cmd_with_garbage(self):
        result = CommandParser.right_commands(['cmd1', 'cmd99'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd1')


    def test_right_commands_with_cmd_has_sub_one(self):
        result = CommandParser.right_commands(['cmd2'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd2')


    def test_right_commands_with_cmd_has_sub_one_with_garbage(self):
        result = CommandParser.right_commands(['cmd2', 'cmd99'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd2')


    def test_right_commands_with_sub_cmd(self):
        result = CommandParser.right_commands(['cmd2', 'cmd3'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd3')


    def test_right_commands_with_sub_cmd_with_garbage(self):
        result = CommandParser.right_commands(['cmd2', 'cmd3', 'cmd99'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd3')


    def test_right_commands_with_sub_cmd_has_sub_one(self):
        result = CommandParser.right_commands(['cmd2', 'cmd4'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd4')


    def test_right_commands_with_sub_cmd_has_sub_one_with_garbage(self):
        result = CommandParser.right_commands(['cmd2', 'cmd4', 'cmd99'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd4')


    def test_right_commands_with_sub_sub_cmd(self):
        result = CommandParser.right_commands(['cmd2', 'cmd4', 'cmd5'])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd4')
        self.assertEqual(result[2], 'cmd5')
    # }}}


    # is_internal_command {{{
    def test_is_internal_command(self):
        self.assertTrue(CommandParser.is_internal_command('_cmd0'))

        self.assertFalse(CommandParser.is_internal_command('cmd1'))
    # }}}


    # available_commands {{{
    def test_available_commands_with_no_cmd(self):
        result = CommandParser.available_commands([])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd1')
        self.assertEqual(result[1], 'cmd2')


    def test_available_commands_with_main_cmd(self):
        result = CommandParser.available_commands(['cmd1'])
        self.assertEqual(len(result), 0)


    def test_available_commands_with_cmd_has_sub_one(self):
        result = CommandParser.available_commands(['cmd2'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd3')
        self.assertEqual(result[1], 'cmd4')


    def test_available_commands_with_sub_cmd(self):
        result = CommandParser.available_commands(['cmd2', 'cmd3'])
        self.assertEqual(len(result), 0)


    def test_available_commands_with_sub_cmd_has_sub_one(self):
        result = CommandParser.available_commands(['cmd2', 'cmd4'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd5')


    def test_available_commands_with_sub_sub_cmd(self):
        result = CommandParser.available_commands(['cmd2', 'cmd4', 'cmd5'])
        self.assertEqual(len(result), 0)
    # }}}


    # command_classes {{{
    def test_command_classes_with_no_cmd(self):
        self.assertEqual(CommandParser.command_classes([]), None)

    def test_command_classes_with_garbage(self):
        self.assertEqual(CommandParser.command_classes(['cmd99']), None)

    def test_command_classes_with_main_cmd(self):
        result = CommandParser.command_classes(['cmd1'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TestCommandParser.cmd1)


    def test_command_classes_with_main_cmd_with_garbage(self):
        self.assertEqual(CommandParser.command_classes(['cmd1', 'cmd99']), None)


    def test_command_classes_with_cmd_has_sub_one(self):
        self.assertEqual(CommandParser.command_classes(['cmd2']), None)


    def test_command_classes_with_cmd_has_sub_one_with_garbage(self):
        self.assertEqual(CommandParser.command_classes(['cmd2', 'cmd99']), None)


    def test_command_classes_with_sub_cmd(self):
        result = CommandParser.command_classes(['cmd2', 'cmd3'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TestCommandParser.cmd3)


    def test_command_classes_with_sub_cmd_with_garbage(self):
        self.assertEqual(CommandParser.command_classes(['cmd2', 'cmd3', 'cmd99']), None)


    def test_command_classes_with_sub_cmd_has_sub_one(self):
        self.assertEqual(CommandParser.command_classes(['cmd2', 'cmd4']), None)


    def test_command_classes_with_sub_cmd_has_sub_one_with_garbage(self):
        self.assertEqual(CommandParser.command_classes(['cmd2', 'cmd4', 'cmd99']), None)


    def test_command_classes_with_sub_sub_cmd(self):
        result = CommandParser.command_classes(['cmd2', 'cmd4', 'cmd5'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TestCommandParser.cmd5)
    # }}}


if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
