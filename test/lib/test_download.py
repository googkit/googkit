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


urlretrieveMock = mock.MagicMock()

try:
    # Python 2.x
    import urllib
    #urllib.urlretrieve
    urllib.urlretrieve = urlretrieveMock
except ImportError:
    # Python 3.x or later
    import urllib.request
    urllib.request.urlretrieve = urlretrieveMock


import lib.download


class TestDownload(unittest.TestCase):
    # run {{{
    def test_run(self):
        lib.download.run('https://exmaple.com/example.zip', '/dir1/dir2')

        urlretrieveMock.assert_called_once_with('https://exmaple.com/example.zip', '/dir1/dir2')
    # }}}


if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
