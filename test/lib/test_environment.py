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

from lib.environment import Environment


class TestEnvironmtnt(unittest.TestCase):
    def test_init(self):
        args = mock.MagicMock()
        config = mock.MagicMock()

        env = Environment(args, config)

        self.assertEqual(env.args, args)
        self.assertEqual(env.config, config)


if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
