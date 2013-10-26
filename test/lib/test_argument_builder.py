import unittest
import doctest
import googkit.lib.argument_builder

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(googkit.lib.argument_builder))
    return tests


if __name__ == '__main__':
    unittest.main()
