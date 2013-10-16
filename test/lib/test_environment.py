import unittest

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock

from googkit.lib.environment import Environment


class TestEnvironmtnt(unittest.TestCase):
    def test_init(self):
        cwd = '/cwd'
        mock_arg_parser = mock.MagicMock()
        mock_tree = mock.MagicMock()

        env = Environment(cwd, mock_arg_parser, mock_tree)

        self.assertEqual(env.cwd, cwd)
        self.assertEqual(env.arg_parser, mock_arg_parser)
        self.assertEqual(env.tree, mock_tree)


if __name__ == '__main__':
    unittest.main()
