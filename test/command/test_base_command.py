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
import sys

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock

from lib.error import GoogkitError
from command.base_command import BaseCommand

from test.stub_stdout import StubStdout


class EnvironmentStub(object):
    def __init__(self):
        self.config = None


class TestBaseCommand(unittest.TestCase):
    # run {{{
    def test_run_on_cmd(self):
        class ConcreteCommand(BaseCommand):
            pass

        with mock.patch('sys.stdout', new_callable = StubStdout):
            env1 = EnvironmentStub()
            env1.config = mock.MagicMock()

            cmd1 = ConcreteCommand(env1)
            cmd1.run_internal = mock.MagicMock()
            cmd1.run()
            cmd1.run_internal.assert_called_once_with()

            env2 = EnvironmentStub()
            env2.config = None

            cmd2 = ConcreteCommand(env2)
            cmd2.run_internal = mock.MagicMock()
            cmd2.run()
            cmd2.run_internal.assert_called_once_with()


    def test_run_on_cmd_needs_config(self):
        class ConcreteCommandNeedsConfig(BaseCommand):
            @classmethod
            def needs_config(cls):
                return True

        with mock.patch('sys.stdout', new_callable = StubStdout):
            env1 = EnvironmentStub()
            env1.config = mock.MagicMock()

            cmd1 = ConcreteCommandNeedsConfig(env1)
            cmd1.run_internal = mock.MagicMock()
            cmd1.run()
            cmd1.run_internal.assert_called_once_with()

            env2 = EnvironmentStub()
            env2.config = None

            cmd2 = ConcreteCommandNeedsConfig(env2)
            cmd2.run_internal = mock.MagicMock()
            with self.assertRaises(GoogkitError):
                cmd2.run()
    # }}}


if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
