import unittest

import googkit.lib.clone
from googkit.compat.unittest import mock


class TestClone(unittest.TestCase):
    def test_run(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('googkit.lib.clone._pull') as mock_pull:
            googkit.lib.clone.run('https://exmaple.com/example.git', '/dir1/dir2')

        self.assertTrue(mock_pull.called)

    def test_run_with_no_target_dir(self):
        with mock.patch('os.path.exists', return_value=False), \
                mock.patch('googkit.lib.clone._clone') as mock_clone:
            googkit.lib.clone.run('https://exmaple.com/example.git', '/dir1/dir2')

        self.assertTrue(mock_clone.called)

    def test_pull(self):
        MockPopen = mock.MagicMock()
        MockPopen.return_value.returncode = 0

        with mock.patch('os.getcwd', return_value='/dir1/dir2/dir3/dir4'), \
                mock.patch('os.chdir') as mock_chdir, \
                mock.patch('subprocess.Popen', new=MockPopen) as mock_popen:
            googkit.lib.clone._pull('https://exmaple.com/example.git', '/dir1/dir2')

        mock_chdir.assert_any_call('/dir1/dir2')
        mock_chdir.assert_any_call('/dir1/dir2/dir3/dir4')
        self.assertTrue(mock_popen.called)

    def test_clone(self):
        MockPopen = mock.MagicMock()
        MockPopen.return_value.returncode = 0

        with mock.patch('os.chdir'), \
                mock.patch('subprocess.Popen', new=MockPopen) as mock_popen:
            googkit.lib.clone.run('https://example.com/example.git', '/dir1/dir2')

        self.assertTrue(mock_popen.called)


if __name__ == '__main__':
    unittest.main()
