import unittest

from googkit.compat.unittest import mock
from googkit.lib.command_tree import CommandTree


class TestCommandTree(unittest.TestCase):
    cmd0 = mock.MagicMock()
    cmd1 = mock.MagicMock()
    cmd3 = mock.MagicMock()
    cmd5 = mock.MagicMock()

    def setUp(self):
        CommandTree.DEFAULT_TREE = {
            '_cmd0': TestCommandTree.cmd0,
            'cmd1': TestCommandTree.cmd1,
            'cmd2': {
                'cmd3': TestCommandTree.cmd3,
                'cmd4': {
                    'cmd5': TestCommandTree.cmd5
                }
            }
        }

        self.tree = CommandTree()

    def test_init(self):
        self.assertEqual(self.tree._tree, CommandTree.DEFAULT_TREE)

    def test_right_commands_with_no_cmd(self):
        result = self.tree.right_commands([])
        self.assertEqual(len(result), 0)

    def test_right_commands_with_garbage(self):
        result = self.tree.right_commands(['cmd999'])
        self.assertEqual(len(result), 0)

    def test_right_commands_with_main_cmd(self):
        result = self.tree.right_commands(['cmd1'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd1')

    def test_right_commands_with_main_cmd_with_garbage(self):
        result = self.tree.right_commands(['cmd1', 'cmd999'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd1')

    def test_right_commands_with_cmd_has_sub_one(self):
        result = self.tree.right_commands(['cmd2'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd2')

    def test_right_commands_with_cmd_has_sub_one_with_garbage(self):
        result = self.tree.right_commands(['cmd2', 'cmd999'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd2')

    def test_right_commands_with_sub_cmd(self):
        result = self.tree.right_commands(['cmd2', 'cmd3'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd3')

    def test_right_commands_with_sub_cmd_with_garbage(self):
        result = self.tree.right_commands(['cmd2', 'cmd3', 'cmd999'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd3')

    def test_right_commands_with_sub_cmd_has_sub_one(self):
        result = self.tree.right_commands(['cmd2', 'cmd4'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd4')

    def test_right_commands_with_sub_cmd_has_sub_one_with_garbage(self):
        result = self.tree.right_commands(['cmd2', 'cmd4', 'cmd999'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd4')

    def test_right_commands_with_sub_sub_cmd(self):
        result = self.tree.right_commands(['cmd2', 'cmd4', 'cmd5'])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 'cmd2')
        self.assertEqual(result[1], 'cmd4')
        self.assertEqual(result[2], 'cmd5')

    def test_is_internal_command(self):
        self.assertTrue(CommandTree.is_internal_command('_cmd0'))

        self.assertFalse(CommandTree.is_internal_command('cmd1'))

    def test_available_commands_with_no_cmd(self):
        result = self.tree.available_commands([])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd1')
        self.assertEqual(result[1], 'cmd2')

    def test_available_commands_with_main_cmd(self):
        result = self.tree.available_commands(['cmd1'])
        self.assertEqual(len(result), 0)

    def test_available_commands_with_cmd_has_sub_one(self):
        result = self.tree.available_commands(['cmd2'])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'cmd3')
        self.assertEqual(result[1], 'cmd4')

    def test_available_commands_with_sub_cmd(self):
        result = self.tree.available_commands(['cmd2', 'cmd3'])
        self.assertEqual(len(result), 0)

    def test_available_commands_with_sub_cmd_has_sub_one(self):
        result = self.tree.available_commands(['cmd2', 'cmd4'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'cmd5')

    def test_available_commands_with_sub_sub_cmd(self):
        result = self.tree.available_commands(['cmd2', 'cmd4', 'cmd5'])
        self.assertEqual(len(result), 0)

    def test_command_class_with_no_cmd(self):
        self.assertEqual(self.tree.command_class([]), None)

    def test_command_class_with_garbage(self):
        self.assertEqual(self.tree.command_class(['cmd999']), None)

    def test_command_class_with_main_cmd(self):
        result = self.tree.command_class(['cmd1'])
        self.assertIsNotNone(result)
        self.assertEqual(result, TestCommandTree.cmd1)

    def test_command_class_with_main_cmd_with_garbage(self):
        self.assertEqual(self.tree.command_class(['cmd1', 'cmd999']), None)

    def test_command_class_with_cmd_has_sub_one(self):
        self.assertEqual(self.tree.command_class(['cmd2']), None)

    def test_command_class_with_cmd_has_sub_one_with_garbage(self):
        self.assertEqual(self.tree.command_class(['cmd2', 'cmd999']), None)

    def test_command_class_with_sub_cmd(self):
        result = self.tree.command_class(['cmd2', 'cmd3'])
        self.assertIsNotNone(result)
        self.assertEqual(result, TestCommandTree.cmd3)

    def test_command_class_with_sub_cmd_with_garbage(self):
        self.assertEqual(self.tree.command_class(['cmd2', 'cmd3', 'cmd999']), None)

    def test_command_class_with_sub_cmd_has_sub_one(self):
        self.assertEqual(self.tree.command_class(['cmd2', 'cmd4']), None)

    def test_command_class_with_sub_cmd_has_sub_one_with_garbage(self):
        self.assertEqual(self.tree.command_class(['cmd2', 'cmd4', 'cmd999']), None)

    def test_command_class_with_sub_sub_cmd(self):
        result = self.tree.command_class(['cmd2', 'cmd4', 'cmd5'])
        self.assertIsNotNone(result)
        self.assertEqual(result, TestCommandTree.cmd5)

    def test_register(self):
        cmd100 = mock.MagicMock()
        cmd101 = mock.MagicMock()

        self.tree.register(['sub', 'subsub', 'subsubsub'], [cmd100, cmd101])
        self.assertTrue('sub' in self.tree._tree)
        self.assertTrue('subsub' in self.tree._tree['sub'])
        self.assertTrue('subsubsub' in self.tree._tree['sub']['subsub'])
        self.assertEqual(self.tree._tree['sub']['subsub']['subsubsub'], [cmd100, cmd101])


if __name__ == '__main__':
    unittest.main()
