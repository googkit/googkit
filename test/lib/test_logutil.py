import unittest
import doctest
import googkit.lib.logutil


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(googkit.lib.logutil))
    return tests


if __name__ == '__main__':
    unittest.main()
