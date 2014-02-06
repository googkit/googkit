import unittest
import doctest
import googkit.lib.command_tree


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(googkit.lib.command_tree))
    return tests

if __name__ == '__main__':
    unittest.main()
