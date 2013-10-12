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

import lib.unzip
import zipfile


class TestClone(unittest.TestCase):
    def setUp(self):
        self.ZipFile = mock.MagicMock()
        zipfile.ZipFile = self.ZipFile

        self.extractall = mock.MagicMock()
        zipfile.ZipFile.return_value.__enter__.return_value.extractall = self.extractall

    def test_run(self):
        lib.unzip.run('/dir1/dir2/test.zip', '/dir1/dir2/dir3/dir4')

        self.ZipFile.assert_called_once_with('/dir1/dir2/test.zip')
        self.extractall.assert_called_once_with('/dir1/dir2/dir3/dir4')


if __name__ == '__main__':
    unittest.main()
