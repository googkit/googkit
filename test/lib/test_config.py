import unittest
import os

from googkit.lib.config import Config


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
DEFAULT_CONFIG = os.path.join(SCRIPT_PATH, '../fixture/stub_default.cfg')


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.cfg = Config()
        self.cfg.parser = _configparser.ConfigParser()

        with open(DEFAULT_CONFIG) as fp:
            if hasattr(self.cfg.parser, 'read_file'):
                # Python 3.2 or later
                self.cfg.parser.read_file(fp)
            else:
                # Python 3.1 or earlier
                self.cfg.parser.readfp(fp)

    def test_load_with_no_user_config(self):
        cfg = Config()
        cfg.load(TEST_CONFIG_1, None, TEST_CONFIG_3)

        self.assertEqual(cfg.parser.get('test1', 'test'), 'TEST1')
        with self.assertRaises(_configparser.NoSectionError):
            cfg.parser.get('test2', 'test')
        self.assertEqual(cfg.parser.get('test3', 'test'), 'TEST3')

    def test_load(self):
        cfg = Config()
        cfg.load(TEST_CONFIG_1, TEST_CONFIG_2, TEST_CONFIG_3)

        self.assertEqual(cfg.parser.get('test1', 'test'), 'TEST1')
        self.assertEqual(cfg.parser.get('test2', 'test'), 'TEST2')
        self.assertEqual(cfg.parser.get('test3', 'test'), 'TEST3')

    # sample of config methods {{{
    def test_development_dir(self):
        self.assertEqual(self.cfg.development_dir(), 'development')


if __name__ == '__main__':
    unittest.main()
