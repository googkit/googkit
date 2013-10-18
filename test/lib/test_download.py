import unittest

import googkit.compat.urllib.request as request
import googkit.lib.download
from googkit.compat.unittest import mock


class TestDownload(unittest.TestCase):
    def test_run(self):
        request.urlretrieve = mock.MagicMock()
        googkit.lib.download.run('https://exmaple.com/example.zip', '/dir1/dir2')

        request.urlretrieve.assert_called_once_with('https://exmaple.com/example.zip', '/dir1/dir2')


if __name__ == '__main__':
    unittest.main()
