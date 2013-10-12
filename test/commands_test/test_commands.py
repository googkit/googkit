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


from cmds.commands import CommandsCommand
from cmds.command import Command
from test.stub_stdout import StubStdout
from test.stub_environment import StubEnvironment
from test.stub_config import *


class TestCommandsCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.cmd = CommandsCommand(self.env)


    def test_init(self):
        self.assertTrue(isinstance(self.cmd, Command))


    def test_run_internal(self):
        self.env.args = ['remove_me', 'arg1', 'arg2']
        self.env.tree = mock.MagicMock()
        self.env.tree.available_commands.return_value = ['DUMMY1', 'DUMMY2']

        with mock.patch('sys.stdout', create = True) as mock_stdout:
            self.cmd.run_internal()

        self.env.tree.available_commands.assert_called_once_with(['arg1', 'arg2'])
        mock_stdout.write.assert_any_call('DUMMY1\nDUMMY2')
