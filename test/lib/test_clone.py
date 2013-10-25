import unittest
import os.path
import subprocess

import googkit.lib.clone
from googkit.compat.unittest import mock


class TestClone(unittest.TestCase):
    def test_run(self):
        dirpath = os.path.join(os.sep, 'dir1', 'dir2')
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('googkit.lib.clone._pull') as mock_pull:
            googkit.lib.clone.run('https://exmaple.com/example.git', dirpath)

        self.assertTrue(mock_pull.called)

    def test_run_with_no_target_dir(self):
        dirpath = os.path.join(os.sep, 'dir1', 'dir2')
        with mock.patch('os.path.exists', return_value=False), \
                mock.patch('googkit.lib.clone._clone') as mock_clone:
            googkit.lib.clone.run('https://exmaple.com/example.git', dirpath)

        self.assertTrue(mock_clone.called)

    def test_pull(self):
        dirpath = os.path.join(os.sep, 'dir1', 'dir2')
        MockPopen = mock.MagicMock()
        MockPopen.return_value.returncode = 0

        with mock.patch('subprocess.Popen', new=MockPopen) as MockPopen, \
                mock.patch('googkit.lib.clone._git_cmd', return_value='GIT'):
            googkit.lib.clone._pull('https://exmaple.com/example.git', dirpath)

        MockPopen.assert_called_once_with(
            ['GIT', 'pull'],
            cwd=dirpath,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def test_clone(self):
        dirpath = os.path.join(os.sep, 'dir1', 'dir2')
        MockPopen = mock.MagicMock()
        MockPopen.return_value.returncode = 0

        with mock.patch('subprocess.Popen', new=MockPopen) as MockPopen, \
                mock.patch('googkit.lib.clone._git_cmd', return_value='GIT'):
            googkit.lib.clone.run('https://example.com/example.git', dirpath)

        MockPopen.assert_called_once_with(
            ['GIT', 'clone', 'https://example.com/example.git', '/dir1/dir2'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)


if __name__ == '__main__':
    unittest.main()
