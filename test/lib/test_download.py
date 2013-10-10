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


import lib.download


class TestDownload(unittest.TestCase):
    def test_run(self):
        _urllib.urlretrieve = mock.MagicMock()
        lib.download.run('https://exmaple.com/example.zip', '/dir1/dir2')

        _urllib.urlretrieve.assert_called_once_with('https://exmaple.com/example.zip', '/dir1/dir2')


if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
