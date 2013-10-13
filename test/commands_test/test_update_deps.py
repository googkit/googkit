# Run the following command to test:
#
#     (in /usr/local/googkit)
#     $ python -m {test_module_name}
#
# See also: http://docs.python.org/3.3/library/unittest.html#command-line-interface
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


import os
import subprocess
from test.stub_stdout import StubStdout
from test.stub_environment import StubEnvironment
from test.stub_config import StubConfig, StubConfigOnStubProject

from cmds.update_deps import UpdateDepsCommand


class TestUpdateDepsCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.cmd = UpdateDepsCommand(self.env)


    def test_needs_config(self):
        self.assertTrue(UpdateDepsCommand.needs_config())


    def test_line_indent(self):
        self.assertEqual(UpdateDepsCommand.line_indent('    '), '    ')
        self.assertEqual(UpdateDepsCommand.line_indent('     a    '), '     ')
        self.assertEqual(UpdateDepsCommand.line_indent('a    '), '')


    def test_update_deps_js(self):
        MockPopen = mock.MagicMock()
        MockPopen.return_value.returncode = 0

        with mock.patch('subprocess.Popen', new=MockPopen) as mock_popen:
            self.cmd.update_deps()

        arg_format_dict = {
            'depswriter_path': StubConfig.DEPSWRITER,
            'js_dev_path': StubConfig.JS_DEV_DIR,
            'relpath_from_base_js_to_js_dev': os.path.relpath(StubConfig.JS_DEV_DIR, os.path.dirname(StubConfig.BASE_JS)),
            'deps_js_path': StubConfig.DEPS_JS
        }

        expected = ' '.join([
            'python',
            '{depswriter_path}',
            '--root_with_prefix="{js_dev_path}',
            '{relpath_from_base_js_to_js_dev}"',
            '--output_file="{deps_js_path}"'
        ]).format(**arg_format_dict)

        mock_popen.assert_called_once_with(expected, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


    def test_update_tests(self):
        self.assertEqual(
            self.cmd.update_tests('DUMMY', ['dummy1', 'dummy2']),
            'var testFiles = [\'dummy1\',\'dummy2\'];')

        self.assertEqual(
            self.cmd.update_tests('DUMMY', []),
            'var testFiles = [];')


    def test_update_testrunner(self):
        # Use stub config for stub project directories.
        self.env.config = StubConfigOnStubProject()

        self.cmd.update_tests = mock.MagicMock()
        self.cmd.update_tests.return_value = 'changed'

        # Data will be given by open with for-in statement
        read_data = '''\
DUMMY
 change me/*@test_files@*/
  DUMMY'''

        # Expected data for write()
        expected_wrote = '''\
DUMMY
 changed/*@test_files@*/
  DUMMY'''

        # Use mock_open
        mock_open = mock.mock_open(read_data=read_data)

        # Context Manager is a return value of the mock_open.__enter__
        mock_fp = mock_open.return_value.__enter__.return_value

        # Read lines has "\n" at each last
        mock_fp.__iter__.return_value = iter([(line + '\n') for line in read_data.split('\n')])

        with mock.patch('cmds.update_deps.open', mock_open, create=True), \
                mock.patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True

            self.cmd.update_testrunner()

        # Expected the path is a related path from all_tests.html to js_dev/example_test.html
        expected_file = os.path.join('js_dev', 'example_test.html')
        self.cmd.update_tests.assert_called_once_with(
            ' change me/*@test_files@*/\n',
            [expected_file])

        # Expected open was called twice (for reading and writing)
        mock_open.assert_any_call(StubConfigOnStubProject.TESTRUNNER)
        mock_open.assert_any_call(StubConfigOnStubProject.TESTRUNNER, 'w')
        self.assertEqual(mock_open.call_count, 2)

        # Expected correct data was wrote
        self.assertEqual(
            mock_fp.write.call_args_list,
            [mock.call(line + '\n',) for line in expected_wrote.split('\n')])


    def test_run_internal(self):
        with mock.patch('sys.stdout', new_callable=StubStdout):
            self.cmd.update_deps = mock.MagicMock()
            self.cmd.update_testrunner = mock.MagicMock()

            self.cmd.run_internal()

            self.cmd.update_deps.assert_called_once_with()
            self.cmd.update_testrunner.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
