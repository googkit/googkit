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


from cmds.setup import SetupCommand

from test.stub_stdout import StubStdout
from test.stub_environment import StubEnvironment
from test.stub_config import *


class TestSetupCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.cmd = SetupCommand(self.env)


    def test_needs_config(self):
        self.assertTrue(SetupCommand.needs_config())


    def test_safe_mkdirs(self):
        with mock.patch('os.makedirs') as mock_makedirs, \
                mock.patch('shutil.rmtree') as mock_rmtree:
            SetupCommand.safe_mkdirs('/tmp/foo/bar')

        mock_rmtree.assert_called_once_with('/tmp/foo/bar', True)
        mock_makedirs.assert_called_once_with('/tmp/foo/bar')


    def test_setup_closure_library(self):
        with mock.patch('lib.clone') as mock_clone:
            self.cmd.setup_closure_library()

        mock_clone.run.assert_called_once_with(
            'https://code.google.com/p/closure-library/',
            LIBRARRY_ROOT)


    def test_setup_closure_compiler(self):
        with mock.patch('lib.download') as mock_download, \
                mock.patch('lib.unzip') as mock_unzip, \
                mock.patch.object(SetupCommand, 'safe_mkdirs') as mock_mkdirs, \
                mock.patch('shutil.rmtree') as mock_rmtree:
            self.cmd.setup_closure_compiler()

        # Expected temporary directory was created and removed
        mock_mkdirs.assert_any_call('tmp')
        mock_rmtree.assert_any_call('tmp')

        mock_unzip.run.assert_called_once_with(
            os.path.join('tmp', 'compiler.zip'),
            COMPILER_ROOT)

        mock_download.run.assert_called_once_with(
            'http://closure-compiler.googlecode.com/files/compiler-latest.zip',
            os.path.join('tmp', 'compiler.zip'))


    def test_run_internal(self):
        with mock.patch('sys.stdout', new_callable=StubStdout):
            self.cmd.setup_closure_compiler = mock.MagicMock()
            self.cmd.setup_closure_library = mock.MagicMock()

            self.cmd.run_internal()

            self.cmd.setup_closure_compiler.assert_called_once_with()
            self.cmd.setup_closure_library.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
