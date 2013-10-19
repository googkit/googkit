import unittest
import os

from test.stub_config import StubConfig
from test.stub_environment import StubEnvironment
from test.stub_stdout import StubStdout

from googkit.commands.download import DownloadCommand
from googkit.compat.unittest import mock


class TestDownloadCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.cmd = DownloadCommand(self.env)
        self.cmd.config = StubConfig()

    def test_needs_project_config(self):
        self.assertTrue(DownloadCommand.needs_project_config())

    def test_download_closure_library(self):
        with mock.patch('googkit.lib.clone') as mock_clone:
            self.cmd.download_closure_library()

        mock_clone.run.assert_called_once_with(
            StubConfig.LIBRARY_GIT_REPOS,
            StubConfig.LIBRARRY_ROOT)

    def test_download_closure_compiler(self):
        tmp_path = '/tmp/dummy'
        with mock.patch('googkit.lib.download') as mock_download, \
                mock.patch('googkit.lib.unzip') as mock_unzip, \
                mock.patch('tempfile.mkdtemp', return_value=tmp_path), \
                mock.patch('shutil.rmtree') as mock_rmtree:
            self.cmd.download_closure_compiler()

        # Expected temporary directory was created and removed
        mock_rmtree.assert_called_once_with(tmp_path)

        mock_unzip.run.assert_called_once_with(
            os.path.join(tmp_path, 'compiler.zip'),
            StubConfig.COMPILER_ROOT)

        mock_download.run.assert_called_once_with(
            StubConfig.COMPILER_LATEST_ZIP,
            os.path.join(tmp_path, 'compiler.zip'))

    def test_run_internal(self):
        self.env.arg_parser = mock.MagicMock()
        self.env.arg_parser.option.return_value = False
        with mock.patch('sys.stdout', new_callable=StubStdout):
            self.cmd.download_closure_compiler = mock.MagicMock()
            self.cmd.download_closure_library = mock.MagicMock()

            self.cmd.run_internal()

            self.cmd.download_closure_compiler.assert_called_once_with()
            self.cmd.download_closure_library.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
