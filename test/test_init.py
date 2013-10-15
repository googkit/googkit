import unittest

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock


import googkit
import logging
from googkit.lib.error import GoogkitError
from test.stub_stdout import StubStdout


class TestGoogkit(unittest.TestCase):
    # This case simulate:
    #   * only 2 commands as dummy1 and dummy2 are available
    #   * googkit.py get 2 argments ARG1, ARG2 (internally DUMMY1, DUMMY2)
    def test_print_help(self):
        # Mociking stdout
        MockStdout = mock.MagicMock(spec=StubStdout)
        with mock.patch('sys.stdout', new_callable=MockStdout) as mock_stdout:
            # Mocking ConfigTree
            mock_tree = mock.MagicMock()
            mock_tree.right_commands.return_value = ['DUMMY1', 'DUMMY2']
            mock_tree.available_commands.return_value = ['dummy1', 'dummy2']

            googkit.print_help(mock_tree, ['ARG1', 'ARG2'])

            mock_tree.right_commands.assert_called_once_with(['ARG1', 'ARG2'])
            mock_tree.available_commands.assert_called_once_with(['DUMMY1', 'DUMMY2'])

            # Expected some messages printing to stdout
            mock_stdout.write.assert_any_call('Usage: googkit DUMMY1 DUMMY2 <command>')
            mock_stdout.write.assert_any_call('Available commands:')
            mock_stdout.write.assert_any_call('    dummy1')
            mock_stdout.write.assert_any_call('    dummy2')

    # This case simulate:
    #   * only 2 commands as dummy1 and dummy2 are available
    #   * googkit.py get 2 argments ARG1, ARG2 but there are invalid
    def test_print_help_with_invalid_args(self):
        # Mociking stdout
        MockStdout = mock.MagicMock(spec=StubStdout)
        with mock.patch('sys.stdout', new_callable=MockStdout) as mock_stdout:
            # Mocking ConfigTree
            mock_tree = mock.MagicMock()
            mock_tree.right_commands.return_value = []
            mock_tree.available_commands.return_value = ['dummy1', 'dummy2']

            googkit.print_help(mock_tree, ['ARG1', 'ARG2'])

            # Expected some messages printing to stdout
            mock_tree.right_commands.assert_called_once_with(['ARG1', 'ARG2'])
            mock_tree.available_commands.assert_called_once_with([])
            mock_stdout.write.assert_any_call('Usage: googkit <command>')
            mock_stdout.write.assert_any_call('Available commands:')
            mock_stdout.write.assert_any_call('    dummy1')
            mock_stdout.write.assert_any_call('    dummy2')

    # This case simulate:
    #   * only 2 commands as dummy1 and dummy2 are available
    #   * googkit.py get no argments
    def test_print_help_with_no_args(self):
        # Mociking stdout
        MockStdout = mock.MagicMock(spec=StubStdout)
        with mock.patch('sys.stdout', new_callable=MockStdout) as mock_stdout:
            # Mocking ConfigTree
            mock_tree = mock.MagicMock()
            mock_tree.right_commands.return_value = []
            mock_tree.available_commands.return_value = ['dummy1', 'dummy2']

            googkit.print_help(mock_tree, [])

            # Expected some messages printing to stdout
            mock_tree.right_commands.assert_called_once_with([])
            mock_tree.available_commands.assert_called_once_with([])
            mock_stdout.write.assert_any_call('Usage: googkit <command>')
            mock_stdout.write.assert_any_call('Available commands:')
            mock_stdout.write.assert_any_call('    dummy1')
            mock_stdout.write.assert_any_call('    dummy2')

    def test_find_config(self):
        # Mocking lib.path
        with mock.patch('googkit.lib.path.user_config') as mock_usr_cfg, \
                mock.patch('googkit.lib.path.default_config') as mock_def_cfg, \
                mock.patch('googkit.lib.path.project_config') as mock_proj_cfg, \
                mock.patch('googkit.Config') as mock_config:
            mock_usr_cfg.return_value = 'DUMMY_USR'
            mock_def_cfg.return_value = 'DUMMY_DEF'
            mock_proj_cfg.return_value = 'DUMMY_PROJ'

            googkit.find_config('/cwd')

        mock_usr_cfg.assert_called_once()
        mock_def_cfg.assert_called_once()
        mock_proj_cfg.assert_called_once()
        mock_config.return_value.load.assert_called_once_with('DUMMY_PROJ', 'DUMMY_USR', 'DUMMY_DEF')

    def test_run(self):
        MockCmd1 = mock.MagicMock()
        MockCmd2 = mock.MagicMock()

        MockCmd1.needs_config.return_value = False
        MockCmd2.needs_config.return_value = False

        mock_cmd1 = MockCmd1.return_value
        mock_cmd2 = MockCmd2.return_value

        with mock.patch('os.chdir'), \
                mock.patch('sys.argv', new=['/DUMMY.py', 'dummy1', 'dummy2']), \
                mock.patch('googkit.lib.path.project_root', return_value='/dir1/dir2'), \
                mock.patch('googkit.print_help'), \
                mock.patch('googkit.find_config', return_value='dummy_cfg'), \
                mock.patch('googkit.Environment', return_value='dummy_env'), \
                mock.patch('googkit.CommandTree') as MockTree, \
                mock.patch('googkit.lib.plugin.load') as mock_load, \
                mock.patch('logging.basicConfig'):
            MockTree.return_value.command_classes.return_value = [MockCmd1, MockCmd2]

            googkit.main()

        mock_load.assert_called_once_with(MockTree.return_value)

        mock_cmd1.run.assert_called_once_with()
        mock_cmd2.run.assert_called_once_with()

    def test_run_command_needs_config(self):
        MockCmd1 = mock.MagicMock()
        MockCmd2 = mock.MagicMock()

        MockCmd1.needs_config.return_value = False
        MockCmd2.needs_config.return_value = True

        mock_cmd1 = MockCmd1.return_value
        mock_cmd2 = MockCmd2.return_value

        with mock.patch('os.chdir'), \
                mock.patch('sys.argv', new=['/DUMMY.py', 'dummy1', 'dummy2']), \
                mock.patch('googkit.lib.path.project_root', return_value='/dir1/dir2'), \
                mock.patch('googkit.print_help'), \
                mock.patch('googkit.find_config', return_value='dummy_cfg'), \
                mock.patch('googkit.Environment', return_value='dummy_env'), \
                mock.patch('googkit.CommandTree') as MockTree, \
                mock.patch('googkit.lib.plugin.load') as mock_load, \
                mock.patch('logging.basicConfig') as mock_basic_cfg:
            MockTree.return_value.command_classes.return_value = [MockCmd1, MockCmd2]

            googkit.main()

        mock_basic_cfg.assert_called_once_with(level=logging.INFO, format='%(message)s')

        mock_load.assert_called_once_with(MockTree.return_value)

        mock_cmd1.run.assert_called_once_with()
        mock_cmd2.run.assert_called_once_with()

    def test_run_with_empty_args(self):
        with mock.patch('os.chdir'), \
                mock.patch('sys.argv', new=['/DUMMY.py']), \
                mock.patch('googkit.print_help') as mock_print_help, \
                mock.patch('googkit.find_config', return_value='dummy_cfg'), \
                mock.patch('googkit.Environment', return_value='dummy_env'), \
                mock.patch('googkit.CommandTree') as MockTree, \
                mock.patch('googkit.lib.plugin.load'), \
                mock.patch('logging.basicConfig') as mock_basic_cfg:
            MockTree.return_value.command_classes.return_value = None

            with self.assertRaises(SystemExit):
                googkit.main()

        mock_basic_cfg.assert_called_once_with(level=logging.INFO, format='%(message)s')

        mock_print_help.assert_called_once_with(MockTree.return_value, [])

    def test_run_with_invalid_args(self):
        with mock.patch('os.chdir'), \
                mock.patch('sys.argv', new=['/DUMMY.py', 'dummy']), \
                mock.patch('googkit.print_help') as mock_print_help, \
                mock.patch('googkit.find_config', return_value='dummy_cfg'), \
                mock.patch('googkit.Environment', return_value='dummy_env'), \
                mock.patch('googkit.CommandTree') as MockTree, \
                mock.patch('googkit.lib.plugin.load'), \
                mock.patch('logging.basicConfig') as mock_basic_cfg:
            MockTree.return_value.command_classes.return_value = None

            with self.assertRaises(SystemExit):
                googkit.main()

        mock_basic_cfg.assert_called_once_with(level=logging.INFO, format='%(message)s')

        mock_print_help.assert_called_once_with(MockTree.return_value, ['dummy'])

    def test_run_with_exception(self):
        MockCmd1 = mock.MagicMock()
        MockCmd2 = mock.MagicMock()

        MockCmd1.needs_config.return_value = False
        MockCmd2.needs_config.return_value = True

        mock_cmd1 = MockCmd1.return_value
        mock_cmd1.run.side_effect = GoogkitError('DUMMY')

        with mock.patch('os.chdir'), \
                mock.patch('sys.argv', new=['/DUMMY.py', 'dummy1', 'dummy2']), \
                mock.patch('sys.stdout') as mock_stdout, \
                mock.patch('googkit.lib.path.project_root', return_value='/dir1/dir2'), \
                mock.patch('googkit.print_help'), \
                mock.patch('googkit.find_config', return_value='dummy_cfg'), \
                mock.patch('googkit.Environment', return_value='dummy_env'), \
                mock.patch('googkit.CommandTree') as MockTree, \
                mock.patch('googkit.lib.plugin.load'), \
                mock.patch('logging.basicConfig') as mock_basic_cfg, \
                mock.patch('logging.error') as mock_error:
            MockTree.return_value.command_classes.return_value = [MockCmd1, MockCmd2]

            with self.assertRaises(SystemExit) as e:
                googkit.main()

        mock_basic_cfg.assert_called_once_with(level=logging.INFO, format='%(message)s')

        self.assertTrue(mock_error.called)


if __name__ == '__main__':
    unittest.main()
