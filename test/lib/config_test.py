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

from lib.config import Config


_configparser = None
try:
    # Python 2.x
    import ConfigParser
    _configparser = ConfigParser
except ImportError:
    # Python 3.x or later
    import configparser
    _configparser = configparser

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_CONFIG_1 = os.path.join(SCRIPT_PATH, '../fixture/test1.cfg')
TEST_CONFIG_2 = os.path.join(SCRIPT_PATH, '../fixture/test2.cfg')
TEST_CONFIG_3 = os.path.join(SCRIPT_PATH, '../fixture/test3.cfg')
DEFAULT_CONFIG = os.path.join(SCRIPT_PATH, '../fixture/default.cfg')


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.cfg = Config()
        self.cfg.parser = _configparser.ConfigParser()

        with open(DEFAULT_CONFIG) as fp:
            self.cfg.parser.readfp(fp)


    # run {{{
    def test_load_with_no_user_config(self):
        cfg = Config()
        cfg.load(TEST_CONFIG_1, None, TEST_CONFIG_3)

        self.assertEqual(cfg.parser.get('test1', 'test'), 'TEST1')
        self.assertEqual(cfg.parser.get('test3', 'test'), 'TEST3')

        with self.assertRaises(_configparser.NoSectionError):
            cfg.parser.get('test2', 'test')


    def test_load(self):
        cfg = Config()
        cfg.load(TEST_CONFIG_1, TEST_CONFIG_2, TEST_CONFIG_3)

        self.assertEqual(cfg.parser.get('test1', 'test'), 'TEST1')
        self.assertEqual(cfg.parser.get('test2', 'test'), 'TEST2')
        self.assertEqual(cfg.parser.get('test3', 'test'), 'TEST3')
    # }}}


    # sample of config methods {{{
    def test_development_dir(self):
        self.assertEqual(self.cfg.development_dir(), 'development')
    # }}}


if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
