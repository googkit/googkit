import unittest
import os

from test.stub_config import StubConfig, StubConfigOnStubProject
from test.stub_environment import StubEnvironment
from test.stub_stdout import StubStdout

from googkit.commands.apply_config import ApplyConfigCommand
from googkit.compat.unittest import mock
import googkit.lib.strutil


class TestApplyConfigCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.cmd = ApplyConfigCommand(self.env)

        self.cmd.config = StubConfig()

    def test_needs_project_config(self):
        self.assertTrue(ApplyConfigCommand.needs_project_config())

    def test_update_base_js(self):
        self.cmd.config = mock.MagicMock()
        self.cmd.config.base_js.return_value = '/dummy'

        line = '<script src="change me"></script>'
        expected = '<script src="."></script>'
        self.assertEqual(self.cmd.update_base_js(line, '/dummy'), expected)

    def test_update_deps_js(self):
        self.cmd.config = mock.MagicMock()
        self.cmd.config.deps_js.return_value = '/dummy'

        line = '<script src="change me"></script>'
        expected = '<script src="."></script>'

        self.assertEqual(self.cmd.update_deps_js(line, '/dummy'), expected)

    def test_multitestrunner_css(self):
        self.cmd.config = mock.MagicMock()
        self.cmd.config.multitestrunner_css.return_value = '/dummy'

        line = '<link rel="stylesheet" href="change me">'
        expected = '<link rel="stylesheet" href=".">'

        self.assertEqual(self.cmd.update_multitestrunner_css(line, '/dummy'), expected)

    def test_apply_config(self):
        # Expected following directory structure:
        #
        # dir1
        # |-- dir2
        # |   +-- development
        # |       |-- target.html
        # |       +-- js_dev
        # |           +-- deps.js
        # +-- closure
        #     +-- library
        #         +-- closure
        #             |-- goog
        #                 +-- base.js
        #
        tgt_path = os.path.join(StubConfig.DEVELOPMENT_DIR, 'target.html')

        self.cmd.update_deps_js = mock.MagicMock()
        self.cmd.update_deps_js.return_value = 'DEPS_JS'
        self.cmd.update_base_js = mock.MagicMock()
        self.cmd.update_base_js.return_value = 'BASE_JS'
        self.cmd.update_multitestrunner_css = mock.MagicMock()
        self.cmd.update_multitestrunner_css.return_value = 'MULTI_TEST_RUNNER_CSS'

        # Data will be given by for-in statement with open()
        read_data = '''\
DUMMY
<!--@multitestrunner_css@-->
 <!--@base_js@-->
  <!--@deps_js@-->
   <!--@dummy_marker@-->'''

        # Expected data will be given by open.write()
        expected = '''\
DUMMY
MULTI_TEST_RUNNER_CSS<!--@multitestrunner_css@-->
 BASE_JS<!--@base_js@-->
  DEPS_JS<!--@deps_js@-->
   <!--@dummy_marker@-->'''

        # Use mock_open
        mock_open = mock.mock_open(read_data=read_data)

        # Context Manager is a return value of the mock_open.__enter__
        mock_fp = mock_open.return_value.__enter__.return_value

        # Read lines has "\n" at each last
        mock_fp.__iter__.return_value = iter([(line + '\n') for line in read_data.split('\n')])

        # Switch to the mock_open from the original open
        with mock.patch('googkit.commands.apply_config.open', mock_open, create=True):
            self.cmd.apply_config(tgt_path)

        # Expected the target file was opened twice for reading and writing
        mock_open.assert_any_call(tgt_path)
        mock_open.assert_any_call(tgt_path, 'w')

        # Expected correct data was wrote
        self.assertEqual(
            mock_fp.write.call_args_list,
            [mock.call(line + '\n',) for line in expected.split('\n')])

        # Expect updaters was called when for each marker was found
        self.cmd.update_multitestrunner_css.assert_called_once_with('<!--@multitestrunner_css@-->\n', StubConfig.DEVELOPMENT_DIR)
        self.cmd.update_base_js.assert_called_once_with(' <!--@base_js@-->\n', StubConfig.DEVELOPMENT_DIR)
        self.cmd.update_deps_js.assert_called_once_with('  <!--@deps_js@-->\n', StubConfig.DEVELOPMENT_DIR)

    def test_apply_config_all(self):
        self.cmd.apply_config = mock.MagicMock()
        self.cmd.config = StubConfigOnStubProject()

        self.cmd.apply_config_all()

        expected_paths = [os.path.normcase(path) for path in [
            'index.html',
            'all_tests.html',
            'style.css',
            'js_dev/example.js',
            'js_dev/example_test.html',
            'js_dev/main.js'
        ]]
        for expected_path in expected_paths:
            path = os.path.join(StubConfigOnStubProject.DEVELOPMENT_DIR, expected_path)
            self.cmd.apply_config.assert_any_call(path)

    def test_run_internal(self):
        dummy_project_root = os.path.normcase('/dir1/dir2')
        self.cmd.apply_config_all = mock.MagicMock()

        with mock.patch('sys.stdout', new_callable=StubStdout), \
                mock.patch('googkit.lib.path.project_root', return_value=dummy_project_root), \
                mock.patch('googkit.commands.apply_config.working_directory'):
            self.cmd.run_internal()

        self.cmd.apply_config_all.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
