import unittest

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock


import os
from test.stub_stdout import StubStdout
from test.stub_environment import StubEnvironment
from test.stub_config import StubConfig

from googkit.cmds.setup import SetupCommand


class TestSetupCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.cmd = SetupCommand(self.env)

    def test_needs_config(self):
        self.assertTrue(SetupCommand.needs_config())

    def test_setup_closure_library(self):
        with mock.patch('googkit.lib.clone') as mock_clone:
            self.cmd.setup_closure_library()

        mock_clone.run.assert_called_once_with(
            'https://code.google.com/p/closure-library/',
            StubConfig.LIBRARRY_ROOT)

    def test_setup_closure_compiler(self):
        tmp_path = '/tmp/dummy'
        with mock.patch('googkit.lib.download') as mock_download, \
                mock.patch('googkit.lib.unzip') as mock_unzip, \
                mock.patch('tempfile.mkdtemp', return_value=tmp_path) as mock_mkdtemp, \
                mock.patch('shutil.rmtree') as mock_rmtree:
            self.cmd.setup_closure_compiler()

        # Expected temporary directory was created and removed
        mock_rmtree.assert_called_once_with(tmp_path)

        mock_unzip.run.assert_called_once_with(
            os.path.join(tmp_path, 'compiler.zip'),
            StubConfig.COMPILER_ROOT)

        mock_download.run.assert_called_once_with(
            'http://closure-compiler.googlecode.com/files/compiler-latest.zip',
            os.path.join(tmp_path, 'compiler.zip'))

    def test_run_internal(self):
        with mock.patch('sys.stdout', new_callable=StubStdout):
            self.cmd.setup_closure_compiler = mock.MagicMock()
            self.cmd.setup_closure_library = mock.MagicMock()

            self.cmd.run_internal()

            self.cmd.setup_closure_compiler.assert_called_once_with()
            self.cmd.setup_closure_library.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
