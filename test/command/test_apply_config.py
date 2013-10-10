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
import os

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock


from lib.error import GoogkitError
from command.apply_config import ApplyConfigCommand

from test.stub_stdout import StubStdout


# Expected following directory structure:
#
# dir1
# |-- dir2 
# |   +-- development
# |       +-- js_dev
# |           +-- deps.js
# +-- closure
#     |-- compiler
#     +-- library
#         +-- closure
#             |-- goog
#             |   +-- base.js
#             +-- css
#                 +-- multitestrunner.css
#
LIBRARRY_ROOT = '/dir1/closure/library/'
COMPILER_ROOT = '/dir1/closure/compiler/'
DEVELOPMENT_DIR = '/dir1/dir2/development'
DEPS_JS = os.path.join(DEVELOPMENT_DIR, 'js_dev/deps.js')
BASE_JS = os.path.join(LIBRARRY_ROOT, 'closure/goog/base.js')
MULTI_TEST_RUNNER_CSS = os.path.join(LIBRARRY_ROOT, 'closure/css/multitestrunner.css')


class FileSystemStub(object):
    def __init__(self, sep):
        self.orig_sep = os.sep
        self.sep = sep
        pass

    def __enter__(self):
        os.sep = self.sep
        return self

    def __exit__(self, *args):
        os.sep = self.orig_sep


class EnvironmentStub(object):
    def __init__(self):
        self.config = None


class ConfigStub(object):
    def __init__(self):
        pass

    def library_root(self):
        return LIBRARRY_ROOT

    def compiler_root(self):
        return COMPILER_ROOT

    def development_dir(self):
        return DEVELOPMENT_DIR

    def deps_js(self):
        return DEPS_JS

    def base_js(self):
        return BASE_JS

    def multitestrunner_css(self):
        return MULTI_TEST_RUNNER_CSS


class TestApplyConfigCommand(unittest.TestCase):
    def test_html_path(self):
        with FileSystemStub('/'):
            self.assertEqual(
                ApplyConfigCommand.html_path('/dir1/dir2/file.ext'),
                '/dir1/dir2/file.ext')


        with FileSystemStub('\\'):
            self.assertEqual(
                ApplyConfigCommand.html_path('\\dir1\\dir2\\file.ext'),
                '/dir1/dir2/file.ext')


    def test_line_indent(self):
        self.assertEqual(ApplyConfigCommand.line_indent('    '), '    ')
        self.assertEqual(ApplyConfigCommand.line_indent('     a    '), '     ')
        self.assertEqual(ApplyConfigCommand.line_indent('a    '), '')


    def test_needs_config(self):
        self.assertTrue(ApplyConfigCommand.needs_config())


    def test_update_base_js(self):
        env = EnvironmentStub()
        env.config = ConfigStub()
        cmd = ApplyConfigCommand(env)

        s = '<script type="text/javascript" src="{src}"></script>'
        expected = s.format(src = os.path.relpath(BASE_JS, DEVELOPMENT_DIR))
        line = '<script type="text/javascript" src="link"></script>'

        self.assertEqual(cmd.update_base_js(line, DEVELOPMENT_DIR), expected)


    def test_update_deps_js(self):
        env = EnvironmentStub()
        env.config = ConfigStub()
        cmd = ApplyConfigCommand(env)

        s = '<script type="text/javascript" src="{src}"></script>'
        expected = s.format(src = os.path.relpath(DEPS_JS, DEVELOPMENT_DIR))
        line = '<script type="text/javascript" src="link"></script>'

        self.assertEqual(cmd.update_deps_js(line, DEVELOPMENT_DIR), expected)


    def test_multitestrunner_css(self):
        env = EnvironmentStub()
        env.config = ConfigStub()
        cmd = ApplyConfigCommand(env)

        s = '<link rel="stylesheet" type="text/css" href="{href}">'
        expected = s.format(href = os.path.relpath(MULTI_TEST_RUNNER_CSS, DEVELOPMENT_DIR))
        line = '<link rel="stylesheet" type="text/css" href="link">'

        self.assertEqual(cmd.update_multitestrunner_css(line, DEVELOPMENT_DIR), expected)


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
        tgt_path = os.path.join(DEVELOPMENT_DIR, 'target.html')
        base_js_rel = os.path.relpath(BASE_JS, DEVELOPMENT_DIR)
        deps_js_rel = os.path.relpath(DEPS_JS, DEVELOPMENT_DIR)
        env = EnvironmentStub()
        env.config = ConfigStub()

        cmd = ApplyConfigCommand(env)
        cmd.update_deps_js = mock.MagicMock()
        cmd.update_deps_js.return_value = 'DEPS_JS'
        cmd.update_base_js = mock.MagicMock()
        cmd.update_base_js.return_value = 'BASE_JS'
        cmd.update_multitestrunner_css = mock.MagicMock()
        cmd.update_multitestrunner_css.return_value = 'MULTI_TEST_RUNNER_CSS'

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
        mock_open = mock.mock_open(read_data = read_data)

        # Context Manager is a return value of the mock_open.__enter__
        mock_fp = mock_open.return_value.__enter__.return_value

        # Read lines has "\n" at each last
        mock_fp.__iter__.return_value = iter([(line + '\n') for line in read_data.split('\n')])

        # Switch to the mock_open from the original open
        with FileSystemStub('/'), mock.patch('command.apply_config.open', mock_open, create = True):
            cmd.apply_config(tgt_path)

        # Expected the target file was opened twice for reading and writing
        mock_open.assert_any_call(tgt_path)
        mock_open.assert_any_call(tgt_path, 'w')

        # Expected correct data was wrote
        self.assertEqual(
            mock_fp.write.call_args_list,
            [mock.call(line + '\n',) for line in expected.split('\n')])

        # Expect updaters was called when for each marker was found
        cmd.update_multitestrunner_css.assert_called_once_with('<!--@multitestrunner_css@-->\n', DEVELOPMENT_DIR)
        cmd.update_base_js.assert_called_once_with(' <!--@base_js@-->\n', DEVELOPMENT_DIR)
        cmd.update_deps_js.assert_called_once_with('  <!--@deps_js@-->\n', DEVELOPMENT_DIR)


    def test_apply_config_all(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        stub_proj = os.path.join(script_path, '../fixture/stub_project')
        stub_proj = os.path.normpath(stub_proj)

        env = EnvironmentStub()
        env.config = mock.MagicMock(spec = ConfigStub)
        env.config.development_dir.return_value = stub_proj

        cmd = ApplyConfigCommand(env)
        cmd.apply_config = mock.MagicMock()

        cmd.apply_config_all()

        expected_calls = [os.path.join(stub_proj, path) for path in [
            'development/index.html',
            'development/all_tests.html',
            'development/style.css',
            'development/js_dev/example.js',
            'development/js_dev/example_test.html',
            'development/js_dev/main.js'
        ]]

        for expected_call in expected_calls:
            cmd.apply_config.assert_any_call(expected_call)


    # run {{{
    def test_run_internal(self):
        with mock.patch('sys.stdout', new_callable = StubStdout):
            base_js_rel = os.path.relpath(BASE_JS, DEVELOPMENT_DIR)
            deps_js_rel = os.path.relpath(DEPS_JS, DEVELOPMENT_DIR)
            env = EnvironmentStub()
            env.config = ConfigStub()

            cmd = ApplyConfigCommand(env)
            cmd.apply_config_all = mock.MagicMock()
            cmd.run()
            cmd.apply_config_all.assert_called_once_with()
    # }}}


if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
