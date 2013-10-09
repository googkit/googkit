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

import lib.clone


class TestClone(unittest.TestCase):
    # run {{{
    def test_run(self):
        os.getcwd = mock.MagicMock()
        os.getcwd.return_value = '/dir1/dir2/dir3/dir4'

        os.path.exists = mock.MagicMock()
        os.path.exists.return_value = True

        os.chdir = mock.MagicMock()

        os.system = mock.MagicMock()

        lib.clone.run('https://exmaple.com/example.git', '/dir1/dir2')

        os.chdir.assert_any_call('/dir1/dir2')
        os.chdir.assert_any_call('/dir1/dir2/dir3/dir4')
        os.system.assert_called_once_with('git pull')


    def test_run_with_no_target_dir(self):
        os.getcwd = mock.MagicMock()
        os.getcwd.return_value = '/dir1/dir2/dir3/dir4'

        os.path.exists = mock.MagicMock()
        os.path.exists.return_value = False

        os.chdir = mock.MagicMock()
        os.system = mock.MagicMock()

        lib.clone.run('https://example.com/example.git', '/dir1/dir2')

        os.system.assert_called_once_with('git clone https://example.com/example.git /dir1/dir2')
    # }}}


if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
