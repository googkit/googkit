import unittest

from googkit.lib.error import GoogkitError
from googkit.lib.error import InvalidOptionError


class TestGoogkitError(unittest.TestCase):
    def test_init(self):
        message = 'Yeah'
        error = GoogkitError(message)

        self.assertTrue(isinstance(error, Exception))
        self.assertEqual(str(error), message)


class TestInvalidOptionError(unittest.TestCase):
    def test_init(self):
        opts = ['--foo', '--bar']
        error = InvalidOptionError(opts)

        for opt in opts:
            self.assertTrue(str(error).find(opt) >= 0)


if __name__ == '__main__':
    unittest.main()
