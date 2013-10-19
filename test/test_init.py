import unittest
import logging

import googkit
from googkit.compat.unittest import mock
from googkit.lib.error import GoogkitError


class TestGoogkit(unittest.TestCase):
    def test_run(self):
        MockCmd = mock.MagicMock()
        MockCmd.needs_project_config.return_value = False
        mock_cmd = MockCmd.return_value

        with mock.patch('os.chdir'), \
                mock.patch('sys.argv', new=['/DUMMY.py', 'dummy1', 'dummy2']), \
                mock.patch('googkit.lib.path.project_root', return_value='/dir1/dir2'), \
                mock.patch('googkit.Help'), \
                mock.patch('googkit.Environment', return_value='dummy_env'), \
                mock.patch('googkit.CommandTree') as MockTree, \
                mock.patch('googkit.lib.plugin.load') as mock_load, \
                mock.patch('logging.basicConfig'):
            MockTree.return_value.command_class.return_value = MockCmd

            googkit.main()

        mock_load.assert_called_once_with(MockTree.return_value)

        mock_cmd.run.assert_called_once_with()

    def test_run_with_empty_args(self):
        with mock.patch('os.chdir'), \
                mock.patch('sys.argv', new=['/DUMMY.py']), \
                mock.patch('googkit.Help') as MockHelp, \
                mock.patch('googkit.Environment', return_value='dummy_env'), \
                mock.patch('googkit.CommandTree') as MockTree, \
                mock.patch('googkit.lib.plugin.load'), \
                mock.patch('logging.basicConfig') as mock_basic_cfg:
            MockTree.return_value.command_class.return_value = None

            with self.assertRaises(SystemExit):
                googkit.main()

        mock_basic_cfg.assert_called_once_with(level=logging.INFO, format='%(message)s')

        self.assertTrue(MockHelp.return_value.print_help.called)

    def test_run_with_invalid_args(self):
        with mock.patch('os.chdir'), \
                mock.patch('sys.argv', new=['/DUMMY.py', 'dummy']), \
                mock.patch('googkit.Help') as MockHelp, \
                mock.patch('googkit.Environment', return_value='dummy_env'), \
                mock.patch('googkit.CommandTree') as MockTree, \
                mock.patch('googkit.lib.plugin.load'), \
                mock.patch('logging.basicConfig') as mock_basic_cfg:
            MockTree.return_value.command_class.return_value = None

            with self.assertRaises(SystemExit):
                googkit.main()

        mock_basic_cfg.assert_called_once_with(level=logging.INFO, format='%(message)s')

        self.assertTrue(MockHelp.return_value.print_help.called)

    def test_run_with_exception(self):
        MockCmd = mock.MagicMock()
        MockCmd.needs_project_config.return_value = False
        mock_cmd = MockCmd.return_value
        mock_cmd.run.side_effect = GoogkitError('DUMMY')

        with mock.patch('os.chdir'), \
                mock.patch('sys.argv', new=['/DUMMY.py', 'dummy1', 'dummy2']), \
                mock.patch('sys.stdout'), \
                mock.patch('googkit.lib.path.project_root', return_value='/dir1/dir2'), \
                mock.patch('googkit.Help'), \
                mock.patch('googkit.Environment', return_value='dummy_env'), \
                mock.patch('googkit.CommandTree') as MockTree, \
                mock.patch('googkit.lib.plugin.load'), \
                mock.patch('logging.basicConfig') as mock_basic_cfg, \
                mock.patch('logging.error') as mock_error:
            MockTree.return_value.command_class.return_value = MockCmd

            with self.assertRaises(SystemExit):
                googkit.main()

        mock_basic_cfg.assert_called_once_with(level=logging.INFO, format='%(message)s')

        self.assertTrue(mock_error.called)


if __name__ == '__main__':
    unittest.main()
