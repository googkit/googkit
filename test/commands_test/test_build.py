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
from test.stub_environment import StubEnvironment
from test.stub_config import StubConfig, StubConfigOnStubProject

from cmds.build import BuildCommand


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
        mock_open = mock.mock_open(read_data=read_data)

        # Context Manager is a return value of the mock_open.__enter__
        mock_fp = mock_open.return_value.__enter__.return_value

        # Read lines has "\n" at each last
        mock_fp.__iter__.return_value = iter([(line + '\n') for line in read_data.split('\n')])

        # Switch to the mock_open from the original open
        with mock.patch('os.sep', new='/'), \
                mock.patch('cmds.build.open', mock_open, create=True):
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

        with mock.patch.object(BuildCommand, 'rmtree_silent') as mock_rmtree_silent, \
                mock.patch.object(BuildCommand, 'ignore_dirs') as mock_ignore_dirs, \
                mock.patch('shutil.copytree') as mock_copytree:
            mock_ignore_dirs.return_value = 'IGNORE'

            self.cmd.setup_files(StubConfigOnStubProject.PRODUCTION_DIR)

        mock_copytree.assert_called_once_with(
            StubConfigOnStubProject.DEVELOPMENT_DIR,
            StubConfigOnStubProject.PRODUCTION_DIR,
            ignore='IGNORE')

        mock_rmtree_silent.assert_called_once_with(StubConfigOnStubProject.PRODUCTION_DIR)

        self.cmd.compile_resource.assert_any_call(
            os.path.join(StubConfigOnStubProject.PRODUCTION_DIR, 'index.html'),
            StubConfigOnStubProject.COMPILED_JS)


    def test_compile_scripts_with_debug_enabled(self):
        self.cmd.setup_files = mock.MagicMock()
        self.cmd.modify_source_map = mock.MagicMock()

        MockPopen = mock.MagicMock()
        MockPopen.return_value.returncode = 0

        with mock.patch('subprocess.Popen', new=MockPopen) as mock_popen, \
                mock.patch('lib.path.project_root', return_value='/dir1'):
            self.cmd.compile_scripts()

        # In debug mode, expected that Popen was called twice
        self.assertEqual(mock_popen.call_count, 2)

        # In debug mode, expected that soource file was modified
        self.cmd.modify_source_map.assert_called_once_with()

        # In debug mode, expected that setup_files was called twice
        self.assertEqual(self.cmd.setup_files.call_count, 2)

        arg_format_dict = {
            'source_map': StubConfig.COMPILED_JS + '.map',
            'source_map_path': os.path.join(StubConfig.PRODUCTION_DIR, StubConfig.COMPILED_JS + '.map'),
            'compiled_js_path': os.path.join(StubConfig.PRODUCTION_DIR, StubConfig.COMPILED_JS),
            'js_dev_path': StubConfig.JS_DEV_DIR,
            'library': os.path.relpath(StubConfig.LIBRARRY_ROOT, StubConfig.PROJECT_DIR),
            'compiler_path': StubConfig.COMPILER,
            'compiled_js_path': os.path.join(StubConfig.PRODUCTION_DIR, StubConfig.COMPILED_JS),
            'closurebuilder_path': StubConfig.CLOSUREBUILDER
        }

        expected = [str_.format(**arg_format_dict) for str_ in [
            'python',
            '{closurebuilder_path}',
            '--root={library}',
            '--root={js_dev_path}',
            '--namespace=main',
            '--output_mode=compiled',
            '--compiler_jar={compiler_path}',
            '--compiler_flags=--compilation_level=COMPILATION_LEVEL',
            '--compiler_flags=--define=goog.DEBUG=false',
            '--output_file={compiled_js_path}'
        ]]

        mock_popen.assert_any_call(expected, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.cmd.setup_files.assert_any_call(StubConfig.PRODUCTION_DIR)

        arg_format_dict_on_debug = {
            'source_map': StubConfig.COMPILED_JS + '.map',
            'source_map_path': os.path.join(StubConfig.DEBUG_DIR, StubConfig.COMPILED_JS + '.map'),
            'compiled_js_path': os.path.join(StubConfig.DEBUG_DIR, StubConfig.COMPILED_JS),
            'js_dev_path': StubConfig.JS_DEV_DIR,
            'library': os.path.relpath(StubConfig.LIBRARRY_ROOT, StubConfig.PROJECT_DIR),
            'compiler_path': StubConfig.COMPILER,
            'compiled_js_path': os.path.join(StubConfig.DEBUG_DIR, StubConfig.COMPILED_JS),
            'closurebuilder_path': StubConfig.CLOSUREBUILDER
        }

        expected_on_debug = [str_.format(**arg_format_dict_on_debug) for str_ in [
            'python',
            '{closurebuilder_path}',
            '--root={library}',
            '--root={js_dev_path}',
            '--namespace=main',
            '--output_mode=compiled',
            '--compiler_jar={compiler_path}',
            '--compiler_flags=--compilation_level=COMPILATION_LEVEL',
            '--compiler_flags=--source_map_format=V3',
            '--compiler_flags=--create_source_map={source_map_path}',
            '--compiler_flags=--output_wrapper="%output%//# sourceMappingURL={source_map}"',
            '--output_file={compiled_js_path}'
        ]]

        mock_popen.assert_any_call(expected_on_debug, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.cmd.setup_files.assert_any_call(StubConfig.DEBUG_DIR)


    def test_compile_scripts(self):
        self.env.config.is_debug_enabled = mock.MagicMock()
        self.env.config.is_debug_enabled.return_value = False

        self.cmd.setup_files = mock.MagicMock()
        self.cmd.modify_source_map = mock.MagicMock()

        MockPopen = mock.MagicMock()
        MockPopen.return_value.returncode = 0

        with mock.patch('subprocess.Popen', new=MockPopen) as mock_popen, \
                mock.patch('lib.path.project_root', return_value='/dir1'):
            self.cmd.compile_scripts()

        mock_popen.returncode = 0

        # Expected that Popen was called twice
        self.assertEqual(mock_popen.call_count, 1)

        # Expected that setup_files was called twice
        self.assertEqual(self.cmd.setup_files.call_count, 1)

        arg_format_dict = {
            'source_map': StubConfig.COMPILED_JS + '.map',
            'source_map_path': os.path.join(StubConfig.PRODUCTION_DIR, StubConfig.COMPILED_JS + '.map'),
            'compiled_js_path': os.path.join(StubConfig.PRODUCTION_DIR, StubConfig.COMPILED_JS),
            'js_dev_path': StubConfig.JS_DEV_DIR,
            'library': os.path.relpath(StubConfig.LIBRARRY_ROOT, StubConfig.PROJECT_DIR),
            'compiler_path': StubConfig.COMPILER,
            'compiled_js_path': os.path.join(StubConfig.PRODUCTION_DIR, StubConfig.COMPILED_JS),
            'closurebuilder_path': StubConfig.CLOSUREBUILDER
        }

        expected = [str_.format(**arg_format_dict) for str_ in [
            'python',
            '{closurebuilder_path}',
            '--root={library}',
            '--root={js_dev_path}',
            '--namespace=main',
            '--output_mode=compiled',
            '--compiler_jar={compiler_path}',
            '--compiler_flags=--compilation_level=COMPILATION_LEVEL',
            '--compiler_flags=--define=goog.DEBUG=false',
            '--output_file={compiled_js_path}'
        ]]

        mock_popen.assert_any_call(expected, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.cmd.setup_files.assert_called_once_with(StubConfig.PRODUCTION_DIR)


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

        with mock.patch('cmds.build.json') as mock_json, \
                mock.patch('cmds.build.open', new=mock_open, create=True):
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
