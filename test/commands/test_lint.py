import unittest
import subprocess
import os.path
from test.stub_environment import StubEnvironment
from test.stub_config import StubConfigOnStubProject
from googkit.compat.unittest import mock
from googkit.commands.lint import LintCommand


class TestLintCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.cmd = LintCommand(self.env)
        self.cmd.config = StubConfigOnStubProject()

    def test_needs_project_config(self):
        self.assertTrue(LintCommand.needs_project_config())

    def test_lint(self):
        MockPopen = mock.MagicMock()
        mock_popen = MockPopen.return_value
        # It simulates the command was succeeded
        mock_popen.returncode = 0

        with mock.patch('subprocess.Popen', new=MockPopen):
            self.cmd.lint()

        call_1 = mock.call([
            'gjslint',
            os.path.join(StubConfigOnStubProject.JS_DEV_DIR, 'example.js'),
            os.path.join(StubConfigOnStubProject.JS_DEV_DIR, 'main.js'),
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        call_2 = mock.call([
            'gjslint',
            os.path.join(StubConfigOnStubProject.JS_DEV_DIR, 'main.js'),
            os.path.join(StubConfigOnStubProject.JS_DEV_DIR, 'example.js'),
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if call_1 not in MockPopen.call_args_list and call_2 not in MockPopen.call_args_list:
            self.fail('Assertion Error: Arguments for gjslint is invalid.')

    def test_run_internal(self):
        self.cmd.lint = mock.MagicMock()

        with mock.patch('googkit.lib.path.project_root'), \
                mock.patch('googkit.commands.lint.working_directory'):
            self.cmd.run_internal()
        self.cmd.lint.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
