# Run the following command to test:
#
#     (in /usr/local/googkit)
#     $ python -m {test_module_name}
#
# See also: http://docs.python.org/3.3/library/unittest.html#command-line-interface
#
# We cannot use unittest.mock on python 2.x!
# Please install the Mock module when you use Python 2.x.
#
#     $ easy_install -U Mock
#
# See also: http://www.voidspace.org.uk/python/mock/#installing

import unittest

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock

from lib.error import GoogkitError
from cmds.command import Command

from test.stub_stdout import StubStdout
from test.stub_environment import StubEnvironment


class TestCommand(unittest.TestCase):
    def test_run(self):
        class ConcreteCommand(Command):
            pass

        with mock.patch('sys.stdout', new_callable=StubStdout):
            env1 = StubEnvironment()
            env1.config = mock.MagicMock()

            cmd1 = ConcreteCommand(env1)
            cmd1.run_internal = mock.MagicMock()
            cmd1.run()
            cmd1.run_internal.assert_called_once_with()

            env2 = StubEnvironment()
            env2.config = None

            cmd2 = ConcreteCommand(env2)
            cmd2.run_internal = mock.MagicMock()
            cmd2.run()
            cmd2.run_internal.assert_called_once_with()


    def test_run_on_cmd_needs_config(self):
        class ConcreteCommandNeedsConfig(Command):
            @classmethod
            def needs_config(cls):
                return True

        with mock.patch('sys.stdout', new_callable=StubStdout):
            env1 = StubEnvironment()
            env1.config = mock.MagicMock()

            cmd1 = ConcreteCommandNeedsConfig(env1)
            cmd1.run_internal = mock.MagicMock()
            cmd1.run()
            cmd1.run_internal.assert_called_once_with()

            env2 = StubEnvironment()
            env2.config = None

            cmd2 = ConcreteCommandNeedsConfig(env2)
            cmd2.run_internal = mock.MagicMock()
            with self.assertRaises(GoogkitError):
                cmd2.run()


if __name__ == '__main__':
    unittest.main()
