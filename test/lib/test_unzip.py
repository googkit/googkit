import unittest
import zipfile

import googkit.lib.unzip
from googkit.compat.unittest import mock


class TestClone(unittest.TestCase):
    def setUp(self):
        self.ZipFile = mock.MagicMock()
        zipfile.ZipFile = self.ZipFile

        self.extractall = mock.MagicMock()
        zipfile.ZipFile.return_value.__enter__.return_value.extractall = self.extractall

    def test_run(self):
        googkit.lib.unzip.run('/dir1/dir2/test.zip', '/dir1/dir2/dir3/dir4')

        self.ZipFile.assert_called_once_with('/dir1/dir2/test.zip')
        self.extractall.assert_called_once_with('/dir1/dir2/dir3/dir4')


if __name__ == '__main__':
    unittest.main()
