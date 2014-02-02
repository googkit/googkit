import unittest
import doctest
import googkit.lib.strutil


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(googkit.lib.option_builder))
    return tests

if __name__ == '__main__':
    unittest.main()
