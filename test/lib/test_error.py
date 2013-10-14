import unittest

from googkit.lib.error import GoogkitError


class TestClone(unittest.TestCase):
    def test_init(self):
        error = GoogkitError('Yeah')
        self.assertTrue(isinstance(error, Exception))


if __name__ == '__main__':
    unittest.main()
