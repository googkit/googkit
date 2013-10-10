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
import sys
import json

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock

from lib.error import GoogkitError
from command.build import BuildCommand

from test.stub_stdout import StubStdout
from test.stub_environment import StubEnvironment
from test.stub_config import *


class TestBuildCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.cmd = BuildCommand(self.env)


    def test_needs_config(self):
        self.assertTrue(BuildCommand.needs_config())


    def rmtree_silent(self):
        with mock.patch('shutil.rmtree') as mock_rmtree:
            BuildCommand.rmtree_silent('/tmp/foo/bar')
            mock_rmtree.assert_called_once_with('/tmp/foo/bar')


    def test_line_indent(self):
        self.assertEqual(BuildCommand.line_indent('    '), '    ')
        self.assertEqual(BuildCommand.line_indent('     a    '), '     ')
        self.assertEqual(BuildCommand.line_indent('a    '), '')


    def test_compile_resource(self):
        tgt_path = '/tmp/foo/bar'

        # Data will be given by for-in statement with open()
        read_data = '''\
DUMMY
<!--@base_js@-->
 <!--@deps_js@-->
  <!--@require_main@-->
   <!--@dummy_marker@-->'''

        # Expected data will be given by open.write()
        expected = '''\
DUMMY
  <script type="text/javascript" src="REQUIRE_MAIN"></script>
   <!--@dummy_marker@-->'''

        # Use mock_open
        mock_open = mock.mock_open(read_data = read_data)

        # Context Manager is a return value of the mock_open.__enter__
        mock_fp = mock_open.return_value.__enter__.return_value

        # Read lines has "\n" at each last
        mock_fp.__iter__.return_value = iter([(line + '\n') for line in read_data.split('\n')])

        # Switch to the mock_open from the original open
        with mock.patch.object(os, 'sep', new = '/'), mock.patch('command.build.open', mock_open, create = True):
            self.cmd.compile_resource(tgt_path, 'REQUIRE_MAIN')

        # Expected the target file was opened twice for reading and writing
        mock_open.assert_any_call(tgt_path)
        mock_open.assert_any_call(tgt_path, 'w')

        # Expected correct data was wrote
        self.assertEqual(
            mock_fp.write.call_args_list,
            [mock.call(line + '\n',) for line in expected.split('\n')])


    def test_setup_files(self):
        self.env.config = StubConfigOnStubProject()
        self.cmd.compile_resource = mock.MagicMock()

        with mock.patch.object(BuildCommand, 'rmtree_silent') as mock_rmtree_silent, mock.patch.object(BuildCommand, 'ignore_dirs') as mock_ignore_dirs, mock.patch('shutil.copytree') as mock_copytree:
            mock_ignore_dirs.return_value = 'IGNORE'

            self.cmd.setup_files(PRODUCTION_DIR_IN_STUB_PROJECT)

        mock_copytree.assert_called_once_with(
                DEVELOPMENT_DIR_IN_STUB_PROJECT,
                PRODUCTION_DIR_IN_STUB_PROJECT,
                ignore = 'IGNORE')

        mock_rmtree_silent.assert_called_once_with(PRODUCTION_DIR_IN_STUB_PROJECT)

        self.cmd.compile_resource.assert_any_call(os.path.join(PRODUCTION_DIR_IN_STUB_PROJECT, 'index.html'), COMPILED_JS_IN_STUB_PROJECT)


    def test_compile_scripts_with_debug_enabled(self):
        self.cmd.setup_files = mock.MagicMock()
        self.cmd.modify_source_map = mock.MagicMock()

        with mock.patch('os.system') as mock_system:
            self.cmd.compile_scripts()

        # In debug mode, expected that os.system was called twice
        self.assertEqual(mock_system.call_count, 2)

        # In debug mode, expected that soource file was modified
        self.cmd.modify_source_map.assert_called_once_with()

        # In debug mode, expected that setup_files was called twice
        self.assertEqual(self.cmd.setup_files.call_count, 2)



        arg_format_dict = {
            'source_map': COMPILED_JS + '.map',
            'source_map_path': os.path.join(PRODUCTION_DIR, COMPILED_JS + '.map'),
            'compiled_js_path': os.path.join(PRODUCTION_DIR, COMPILED_JS),
            'js_dev_path': JS_DEV_DIR,
            'library': LIBRARRY_ROOT,
            'compiler_path': COMPILER,
            'compiled_js_path': os.path.join(PRODUCTION_DIR, COMPILED_JS),
            'closurebuilder_path': CLOSUREBUILDER
        }

        expected = ' '.join([
            'python',
            '{closurebuilder_path}',
            '--root={library}',
            '--root={js_dev_path}',
            '--namespace=main',
            '--output_mode=compiled',
            '--compiler_jar={compiler_path}',
            '--compiler_flags=--compilation_level=%COMPILATION_LEVEL%',
            '--compiler_flags=--define=goog.DEBUG=false',
            '--output_file={compiled_js_path}']).format(**arg_format_dict)


        mock_system.assert_any_call(expected)


        arg_format_dict_on_debug = {
            'source_map': COMPILED_JS + '.map',
            'source_map_path': os.path.join(DEBUG_DIR, COMPILED_JS + '.map'),
            'compiled_js_path': os.path.join(DEBUG_DIR, COMPILED_JS),
            'js_dev_path': JS_DEV_DIR,
            'library': LIBRARRY_ROOT,
            'compiler_path': COMPILER,
            'compiled_js_path': os.path.join(DEBUG_DIR, COMPILED_JS),
            'closurebuilder_path': CLOSUREBUILDER
        }

        expected_on_debug = ' '.join([
            'python',
            '{closurebuilder_path}',
            '--root={library}',
            '--root={js_dev_path}',
            '--namespace=main',
            '--output_mode=compiled',
            '--compiler_jar={compiler_path}',
            '--compiler_flags=--compilation_level=%COMPILATION_LEVEL%',
            '--compiler_flags=--source_map_format=V3',
            '--compiler_flags=--create_source_map={source_map_path}',
            '--compiler_flags=--output_wrapper="%output%//# sourceMappingURL={source_map}"',
            '--output_file={compiled_js_path}']).format(**arg_format_dict_on_debug)

        mock_system.assert_any_call(expected_on_debug)

        self.cmd.setup_files.assert_any_call(PRODUCTION_DIR)
        self.cmd.setup_files.assert_any_call(DEBUG_DIR)


    def test_modify_source_map(self):
        # Data will be given by open()
        stub_source_map = {
            'sourceRoot': 'change me',
            'dummy': 'do not change me'
        }

        expected = {
            'sourceRoot': '../',
            'dummy': 'do not change me'
        }

        mock_open = mock.mock_open()

        with mock.patch('command.build.json') as mock_json, mock.patch('command.build.open', new = mock_open, create = True):
            mock_open.return_value.__enter__.return_value = 'DUMMY'
            mock_json.load.return_value = stub_source_map

            self.cmd.modify_source_map()

        mock_json.load.assert_called_once_with('DUMMY')
        self.assertEqual(mock_json.dump.call_args[0][0], expected)
        self.assertEqual(mock_json.dump.call_count, 1)


    def test_run_internal(self):
        self.cmd.compile_scripts = mock.MagicMock()
        self.cmd.run_internal()
        self.cmd.compile_scripts.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
