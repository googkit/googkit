import unittest
import urllib

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock


_urllib = None

if hasattr(urllib, 'urlretrieve'):
    # Python 2.x
    _urllib = urllib
else:
    # Python 3.x or later
    import urllib.request
    _urllib = urllib.request


import googkit.lib.download


class TestDownload(unittest.TestCase):
    def test_run(self):
        _urllib.urlretrieve = mock.MagicMock()
        googkit.lib.download.run('https://exmaple.com/example.zip', '/dir1/dir2')

        _urllib.urlretrieve.assert_called_once_with('https://exmaple.com/example.zip', '/dir1/dir2')


if __name__ == '__main__':
    unittest.main()
