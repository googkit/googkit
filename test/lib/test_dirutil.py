import unittest
import doctest
import googkit.lib.dirutil


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(googkit.lib.dirutil))
    return tests


if __name__ == '__main__':
    unittest.main()
