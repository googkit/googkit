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

        MockZipFile = mock.MagicMock()
        mock_zip = MockZipFile.return_value.__enter__.return_value

        with mock.patch('googkit.commands.download.request.urlretrieve') as mock_urlretrive, \
                mock.patch('zipfile.ZipFile', new=MockZipFile), \
                mock.patch('tempfile.mkdtemp', return_value=tmp_path), \
                mock.patch('shutil.rmtree') as mock_rmtree:
            self.cmd.download_closure_compiler()

        # Expected temporary directory was created and removed
        mock_rmtree.assert_called_once_with(tmp_path)

        MockZipFile.assert_called_once_with(
            os.path.join(tmp_path, 'compiler.zip'))
        mock_zip.extractall.assert_called_once_with(
            StubConfig.COMPILER_ROOT)

        mock_urlretrive.assert_called_once_with(
            StubConfig.COMPILER_LATEST_ZIP,
            os.path.join(tmp_path, 'compiler.zip'))

    def test_run_internal(self):
        self.env.argument = mock.MagicMock()
        self.env.argument.option.return_value = False
        dummy_project_root = os.path.normcase('/dir1/dir2')
        self.cmd.download_closure_compiler = mock.MagicMock()
        self.cmd.download_closure_library = mock.MagicMock()

        with mock.patch('sys.stdout', new_callable=StubStdout), \
                mock.patch('googkit.lib.path.project_root', return_value=dummy_project_root), \
                mock.patch('googkit.commands.download.working_directory'):
            self.cmd.run_internal()

        self.cmd.download_closure_compiler.assert_called_once_with()
        self.cmd.download_closure_library.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
