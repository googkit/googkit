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
import os
import re

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock


import googkit
from lib.error import GoogkitError
from test.stub_stdout import StubStdout


class TestGoogkit(unittest.TestCase):
    def test_print_help(self):
        MockStdout = mock.MagicMock(spec = StubStdout)

        with mock.patch('sys.stdout', new_callable = MockStdout) as mock_stdout, \
                mock.patch('lib.command_tree.CommandTree') as mock_tree:
            mock_tree.return_value.right_commands.return_value = ['DUMMY1', 'DUMMY2']
            mock_tree.return_value.available_commands.return_value = ['dummy1', 'dummy2']

            googkit.print_help(['ARG1', 'ARG2'])

            mock_right_cmds.assert_called_once_with(['ARG1', 'ARG2'])
            mock_available_cmds.assert_called_once_with(['DUMMY1', 'DUMMY2'])
            mock_stdout.write.assert_any_call('Usage: googkit DUMMY1 DUMMY2 <command>')
            mock_stdout.write.assert_any_call('Available commands:')
            mock_stdout.write.assert_any_call('    dummy1')
            mock_stdout.write.assert_any_call('    dummy2')


    def test_print_help_with_no_arg(self):
        MockStdout = mock.MagicMock(spec = StubStdout)

        with mock.patch('sys.stdout', new_callable = MockStdout) as mock_stdout, \
                mock.patch('lib.command_tree.CommandTree') as mock_tree:
            mock_tree.return_value.right_commands.return_value = []
            mock_tree.return_value.available_commands.return_value = ['dummy1', 'dummy2']

            googkit.print_help(['ARG1', 'ARG2'])

            mock_tree.return_value.right_commands.assert_called_once_with(['ARG1', 'ARG2'])
            mock_tree.return_value.available_commands.assert_called_once_with([])
            mock_stdout.write.assert_any_call('Usage: googkit <command>')
            mock_stdout.write.assert_any_call('Available commands:')
            mock_stdout.write.assert_any_call('    dummy1')
            mock_stdout.write.assert_any_call('    dummy2')


    def test_find_config(self):
        with mock.patch('lib.path.user_config') as mock_usr_cfg, \
                mock.patch('lib.path.default_config') as mock_def_cfg, \
                mock.patch('lib.path.project_config') as mock_proj_cfg, \
                mock.patch('googkit.Config') as mock_config:
            mock_usr_cfg.return_value = 'DUMMY_USR'
            mock_def_cfg.return_value = 'DUMMY_DEF'
            mock_proj_cfg.return_value = 'DUMMY_PROJ'

            googkit.find_config()

        mock_usr_cfg.assert_called_once_with()
        mock_def_cfg.assert_called_once_with()
        mock_proj_cfg.assert_called_once_with()
        mock_config.return_value.load.assert_called_once_with('DUMMY_PROJ', 'DUMMY_USR', 'DUMMY_DEF')


    def test_run(self):
        mock_cmd1 = mock.MagicMock()
        mock_cmd2 = mock.MagicMock()

        mock_cmd1.needs_config.return_value = False
        mock_cmd2.needs_config.return_value = False 

        with mock.patch('os.chdir') as mock_chdir, \
                mock.patch('sys.argv', new = ['/DUMMY.py', 'dummy1', 'dummy2']), \
                mock.patch('googkit.project_root', return_value = '/dir1/dir2'), \
                mock.patch('googkit.print_help') as mock_print_help, \
                mock.patch('googkit.find_config', return_value = 'dummy_cfg'), \
                mock.patch('googkit.Environment', return_value = 'dummy_env') as mock_env, \
                mock.patch('googkit.CommandTree') as mock_cmd_parser:
            mock_cmd_parser.command_classes.return_value = [mock_cmd1, mock_cmd2]

            googkit.run()

        mock_cmd_parser.command_classes.assert_called_once_with(['dummy1', 'dummy2'])

        mock_cmd1.assert_called_once_with('dummy_env')
        mock_cmd2.assert_called_once_with('dummy_env')

        mock_cmd1.return_value.run.assert_called_once_with()
        mock_cmd2.return_value.run.assert_called_once_with()

        mock_env.assert_any_call(['dummy1', 'dummy2'], None)
        self.assertEqual(mock_env.call_count, 2)
        self.assertFalse(mock_chdir.called)


    def test_run_command_needs_config(self):
        mock_cmd1 = mock.MagicMock()
        mock_cmd2 = mock.MagicMock()

        mock_cmd1.needs_config.return_value = False 
        mock_cmd2.needs_config.return_value = True 

        with mock.patch('os.chdir') as mock_chdir, \
                mock.patch('sys.argv', new = ['/DUMMY.py', 'dummy1', 'dummy2']), \
                mock.patch('googkit.project_root', return_value = '/dir1/dir2'), \
                mock.patch('googkit.print_help') as mock_print_help, \
                mock.patch('googkit.find_config', return_value = 'dummy_cfg'), \
                mock.patch('googkit.Environment', return_value = 'dummy_env') as mock_env, \
                mock.patch('googkit.CommandTree') as mock_cmd_parser:
            mock_cmd_parser.command_classes.return_value = [mock_cmd1, mock_cmd2]

            googkit.run()

        mock_cmd_parser.command_classes.assert_called_once_with(['dummy1', 'dummy2'])

        mock_cmd1.assert_called_once_with('dummy_env')
        mock_cmd2.assert_called_once_with('dummy_env')

        mock_cmd1.return_value.run.assert_called_once_with()
        mock_cmd2.return_value.run.assert_called_once_with()

        mock_env.assert_any_call(['dummy1', 'dummy2'], 'dummy_cfg')
        mock_env.assert_any_call(['dummy1', 'dummy2'], None)
        self.assertEqual(mock_env.call_count, 2)

        mock_chdir.assert_any_call('/dir1/dir2')


    def test_run_with_empty_args(self):
        with mock.patch('os.chdir') as mock_chdir, \
                mock.patch('sys.argv', new = ['/DUMMY.py']), \
                mock.patch('googkit.print_help') as mock_print_help, \
                mock.patch('googkit.find_config', return_value = 'dummy_cfg'), \
                mock.patch('googkit.Environment', return_value = 'dummy_env') as mock_env, \
                mock.patch('googkit.CommandTree') as mock_cmd_parser:
            mock_cmd_parser.command_classes.return_value = None

            with self.assertRaises(SystemExit):
                googkit.run()

        mock_print_help.assert_called_once_with()


    def test_run_with_invalied_args(self):
        with mock.patch('os.chdir') as mock_chdir, \
                mock.patch('sys.argv', new = ['/DUMMY.py', 'dummy']), \
                mock.patch('googkit.print_help') as mock_print_help, \
                mock.patch('googkit.find_config', return_value = 'dummy_cfg'), \
                mock.patch('googkit.Environment', return_value = 'dummy_env') as mock_env, \
                mock.patch('googkit.CommandTree') as mock_cmd_parser:
            mock_cmd_parser.command_classes.return_value = None

            with self.assertRaises(SystemExit):
                googkit.run()

        mock_print_help.assert_called_once_with(['dummy'])



if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
