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

import subprocess
import googkit.lib.clone


class TestClone(unittest.TestCase):
    def test_run(self):
        MockPopen = mock.MagicMock()
        MockPopen.return_value.returncode = 0

        with mock.patch('os.getcwd', return_value='/dir1/dir2/dir3/dir4'), \
                mock.patch('os.path.exists', return_value=True), \
                mock.patch('os.chdir') as mock_chdir, \
                mock.patch('subprocess.Popen', new=MockPopen) as mock_popen:
            googkit.lib.clone.run('https://exmaple.com/example.git', '/dir1/dir2')

        mock_chdir.assert_any_call('/dir1/dir2')
        mock_chdir.assert_any_call('/dir1/dir2/dir3/dir4')
        mock_popen.assert_called_once_with(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_run_with_no_target_dir(self):
        MockPopen = mock.MagicMock()
        MockPopen.return_value.returncode = 0

        with mock.patch('os.getcwd', return_value='/dir1/dir2/dir3/dir4'), \
                mock.patch('os.path.exists', return_value=False), \
                mock.patch('os.chdir'), \
                mock.patch('subprocess.Popen', new=MockPopen) as mock_popen:
            googkit.lib.clone.run('https://example.com/example.git', '/dir1/dir2')

        mock_popen.assert_called_once_with(['git', 'clone', 'https://example.com/example.git', '/dir1/dir2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == '__main__':
    unittest.main()
