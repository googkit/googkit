import unittest

from googkit.compat.unittest import mock
from googkit.lib.environment import Environment


class TestEnvironmtnt(unittest.TestCase):
    def test_init(self):
        cwd = '/cwd'
        mock_argument = mock.MagicMock()
        mock_tree = mock.MagicMock()

        env = Environment(cwd, mock_argument, mock_tree)

        self.assertEqual(env.cwd, cwd)
        self.assertEqual(env.argument, mock_argument)
        self.assertEqual(env.tree, mock_tree)


if __name__ == '__main__':
    unittest.main()
