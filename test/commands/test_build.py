import unittest
import doctest
import os
import subprocess

from googkit.compat.unittest import mock
from test.stub_config import StubConfig, StubConfigOnStubProject
from test.stub_environment import StubEnvironment

import googkit.lib.strutil
import googkit.commands.build
BuildCommand = googkit.commands.build.BuildCommand


class TestBuildCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.cmd = BuildCommand(self.env)
        self.cmd.config = StubConfig()

    def test_needs_project_config(self):
        self.assertTrue(BuildCommand.needs_project_config())

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
  <script src="REQUIRE_MAIN"></script>
   <!--@dummy_marker@-->'''

        # Use mock_open
        mock_open = mock.mock_open(read_data=read_data)

        # Context Manager is a return value of the mock_open.__enter__
        mock_fp = mock_open.return_value.__enter__.return_value

        # Read lines has "\n" at each last
        mock_fp.__iter__.return_value = iter([(line + '\n') for line in read_data.split('\n')])

        # Switch to the mock_open from the original open
        with mock.patch('os.sep', new='/'), \
                mock.patch('googkit.commands.build.open', mock_open, create=True):
            self.cmd.compile_resource(tgt_path, 'REQUIRE_MAIN')

        # Expected the target file was opened twice for reading and writing
        mock_open.assert_any_call(tgt_path)
        mock_open.assert_any_call(tgt_path, 'w')

        # Expected correct data was wrote
        self.assertEqual(
            mock_fp.write.call_args_list,
            [mock.call(line + '\n',) for line in expected.split('\n')])

    def test_setup_files(self):
        self.cmd.config = StubConfigOnStubProject()
        self.cmd.compile_resource = mock.MagicMock()

        with mock.patch.object(BuildCommand, 'ignore_dirs') as mock_ignore_dirs, \
                mock.patch('googkit.lib.file.copytree') as mock_copytree:
            mock_ignore_dirs.return_value = 'IGNORE'

            self.cmd.setup_files(StubConfigOnStubProject.PRODUCTION_DIR, False)

        mock_copytree.assert_called_once_with(
            StubConfigOnStubProject.DEVELOPMENT_DIR,
            StubConfigOnStubProject.PRODUCTION_DIR,
            ignore='IGNORE')

        self.cmd.compile_resource.assert_any_call(
            os.path.join(StubConfigOnStubProject.PRODUCTION_DIR, 'index.html'),
            StubConfigOnStubProject.COMPILED_JS)

    def test_debug_arguments(self):
        expected = BuildCommand.BuilderArguments()
        expected.builder_arg('--root',
                             os.path.relpath(StubConfig.LIBRARRY_ROOT, StubConfig.PROJECT_DIR))
        expected.builder_arg('--root', StubConfig.JS_DEV_DIR)
        expected.builder_arg('--namespace', 'main')
        expected.builder_arg('--output_mode', 'compiled')
        expected.builder_arg('--output_file',
                             os.path.join(StubConfig.DEBUG_DIR, StubConfig.COMPILED_JS))
        expected.builder_arg('--compiler_jar', StubConfig.COMPILER)
        expected.compiler_arg('--compilation_level', 'COMPILATION_LEVEL')
        expected.compiler_arg('--source_map_format', 'V3')
        expected.compiler_arg('--create_source_map',
                              os.path.join(StubConfig.DEBUG_DIR, StubConfig.COMPILED_JS + '.map'))
        expected.compiler_arg('--output_wrapper', '"%output%//# sourceMappingURL={path}"'.format(path=StubConfig.COMPILED_JS + '.map'))

        with mock.patch('os.path.exists', return_value=False):
            args = self.cmd.debug_arguments(StubConfig.PROJECT_DIR)
        self.assertEqual(args, expected)

    def test_production_arguments(self):
        expected = BuildCommand.BuilderArguments()
        expected.builder_arg('--root',
                             os.path.relpath(StubConfig.LIBRARRY_ROOT, StubConfig.PROJECT_DIR))
        expected.builder_arg('--root', StubConfig.JS_DEV_DIR)
        expected.builder_arg('--namespace', 'main')
        expected.builder_arg('--output_mode', 'compiled')
        expected.builder_arg('--output_file',
                             os.path.join(StubConfig.PRODUCTION_DIR, StubConfig.COMPILED_JS))
        expected.builder_arg('--compiler_jar', StubConfig.COMPILER)
        expected.compiler_arg('--compilation_level', 'COMPILATION_LEVEL')
        expected.compiler_arg('--define', 'goog.DEBUG=false')

        with mock.patch('os.path.exists', return_value=False):
            args = self.cmd.production_arguments(StubConfig.PROJECT_DIR)
        self.assertEqual(args, expected)

    def test_debug_arguments_with_flagfile(self):
        expected = BuildCommand.BuilderArguments()
        expected.builder_arg('--root',
                             os.path.relpath(StubConfig.LIBRARRY_ROOT, StubConfig.PROJECT_DIR))
        expected.builder_arg('--root', StubConfig.JS_DEV_DIR)
        expected.builder_arg('--namespace', 'main')
        expected.builder_arg('--output_mode', 'compiled')
        expected.builder_arg('--output_file',
                             os.path.join(StubConfig.DEBUG_DIR, StubConfig.COMPILED_JS))
        expected.builder_arg('--compiler_jar', StubConfig.COMPILER)
        expected.compiler_arg('--compilation_level', 'COMPILATION_LEVEL')
        expected.compiler_arg('--source_map_format', 'V3')
        expected.compiler_arg('--create_source_map',
                              os.path.join(StubConfig.DEBUG_DIR, StubConfig.COMPILED_JS + '.map'))
        expected.compiler_arg('--output_wrapper', '"%output%//# sourceMappingURL={path}"'.format(path=StubConfig.COMPILED_JS + '.map'))
        expected.compiler_arg('--flagfile', StubConfig.COMPILER_FLAGFILE_FOR_DEBUG)

        with mock.patch('os.path.exists', return_value=True):
            args = self.cmd.debug_arguments(StubConfig.PROJECT_DIR)
        self.assertEqual(args, expected)

    def test_production_arguments_with_flagfile(self):
        expected = BuildCommand.BuilderArguments()
        expected.builder_arg('--root',
                             os.path.relpath(StubConfig.LIBRARRY_ROOT, StubConfig.PROJECT_DIR))
        expected.builder_arg('--root', StubConfig.JS_DEV_DIR)
        expected.builder_arg('--namespace', 'main')
        expected.builder_arg('--output_mode', 'compiled')
        expected.builder_arg('--output_file',
                             os.path.join(StubConfig.PRODUCTION_DIR, StubConfig.COMPILED_JS))
        expected.builder_arg('--compiler_jar', StubConfig.COMPILER)
        expected.compiler_arg('--compilation_level', 'COMPILATION_LEVEL')
        expected.compiler_arg('--define', 'goog.DEBUG=false')
        expected.compiler_arg('--flagfile', StubConfig.COMPILER_FLAGFILE)

        with mock.patch('os.path.exists', return_value=True):
            args = self.cmd.production_arguments(StubConfig.PROJECT_DIR)
        self.assertEqual(args, expected)


    def test_build_production(self):
        self.cmd.setup_files = mock.MagicMock()
        self.cmd.production_arguments = mock.MagicMock()
        self.cmd.production_arguments.return_value = ['ARG']

        MockPopen = mock.MagicMock()
        mock_popen = MockPopen.return_value
        # It simulates the command was succeeded
        mock_popen.returncode = 0

        with mock.patch('subprocess.Popen', new=MockPopen):
            self.cmd.build_production(StubConfig.PROJECT_DIR, False)

        self.cmd.setup_files.assert_called_once_with(StubConfig.PRODUCTION_DIR, False)
        MockPopen.assert_called_once_with(
            ['python', StubConfig.CLOSUREBUILDER, 'ARG'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def test_build_debug(self):
        self.cmd.setup_files = mock.MagicMock()
        self.cmd.debug_arguments = mock.MagicMock()
        self.cmd.debug_arguments.return_value = ['ARG']
        self.cmd.modify_source_map = mock.MagicMock()

        MockPopen = mock.MagicMock()
        mock_popen = MockPopen.return_value
        # It simulates the command was succeeded
        mock_popen.returncode = 0

        with mock.patch('subprocess.Popen', new=MockPopen):
            self.cmd.build_debug(StubConfig.PROJECT_DIR, False)

        self.cmd.setup_files.assert_called_once_with(StubConfig.DEBUG_DIR, False)
        MockPopen.assert_called_once_with(
            ['python', StubConfig.CLOSUREBUILDER, 'ARG'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        self.cmd.modify_source_map.assert_called_once_with(
            os.path.join(StubConfig.DEBUG_DIR, StubConfig.COMPILED_JS + '.map'),
            StubConfig.PROJECT_DIR)

    def test_modify_source_map(self):
        # Data will be given by open()
        stub_source_map = {
            'sourceRoot': 'change me',
            'dummy': 'do not change me'
        }

        expected = {
            'sourceRoot': os.path.relpath(StubConfig.PROJECT_DIR, StubConfig.DEBUG_DIR),
            'dummy': 'do not change me'
        }

        mock_open = mock.mock_open()
        dummy_source_map_file = 'DUMMY'

        with mock.patch('googkit.commands.build.json') as mock_json, \
                mock.patch('googkit.commands.build.open', new=mock_open, create=True):
            mock_open.return_value.__enter__.return_value = dummy_source_map_file
            mock_json.load.return_value = stub_source_map

            self.cmd.modify_source_map(dummy_source_map_file, StubConfig.PROJECT_DIR)

        mock_json.load.assert_called_once_with(dummy_source_map_file)
        self.assertEqual(mock_json.dump.call_args[0][0], expected)
        self.assertEqual(mock_json.dump.call_count, 1)

    def test_run_internal(self):
        self.cmd.build_debug = mock.MagicMock()
        self.cmd.build_production = mock.MagicMock()
        self.env.argument = mock.MagicMock()
        self.env.argument.option.return_value = False
        dummy_project_root = os.path.normcase('/dir1/dir2')

        with mock.patch('googkit.lib.path.project_root', return_value=dummy_project_root), \
                mock.patch('googkit.commands.build.working_directory'):

            self.cmd.run_internal()

        self.cmd.build_production.assert_called_once_with(dummy_project_root, False)

    def test_run_internal_with_debug_opt(self):
        self.cmd.build_debug = mock.MagicMock()
        self.cmd.build_production = mock.MagicMock()
        self.env.argument = mock.MagicMock()
        self.env.argument.option.side_effect = lambda opt: opt == '--debug'
        dummy_project_root = os.path.normcase('/dir1/dir2')

        with mock.patch('googkit.lib.path.project_root', return_value=dummy_project_root), \
                mock.patch('googkit.commands.build.working_directory'):

            self.cmd.run_internal()

        self.cmd.build_debug.assert_called_once_with(dummy_project_root, False)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(googkit.commands.build))
    return tests


if __name__ == '__main__':
    unittest.main()
