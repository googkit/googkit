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
from command.init import InitCommand

from test.stub_stdout import StubStdout
from test.stub_environment import StubEnvironment
from test.stub_config import *


class TestInitCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.cmd = InitCommand(self.env)


    def test_needs_config(self):
        self.assertFalse(InitCommand.needs_config())


    def test_copy_templates(self):
        dst_path = '/tmp/foo/bar'
        self.cmd.template_dir = mock.MagicMock()
        self.cmd.template_dir.return_value = 'dummy'

        with mock.patch('os.listdir') as mock_listdir, mock.patch('distutils.dir_util.copy_tree') as mock_copytree, mock.patch.object(InitCommand, 'TEMPLATE_DIR', new = 'dummy'):
            mock_listdir.return_value = []

            self.cmd.copy_template(dst_path)

        mock_copytree.assert_called_once_with('dummy', dst_path)


    def test_copy_templates_on_unempty_dir(self):
        dst_path = '/tmp/foo/bar'
        self.cmd.template_dir = mock.MagicMock()
        self.cmd.template_dir.return_value = 'dummy'

        with mock.patch('os.listdir') as mock_listdir, mock.patch('distutils.dir_util.copy_tree') as mock_copytree:
            mock_listdir.return_value = ['DUMMY']

            with self.assertRaises(GoogkitError):
                self.cmd.copy_template(dst_path)


    def test_run_internal(self):
        with mock.patch('os.getcwd') as mock_getcwd:
            mock_getcwd.return_value = 'DUMMY'
            self.cmd.copy_template = mock.MagicMock()
            
            self.cmd.run_internal()

            mock_getcwd.assert_called_once_with()
            self.cmd.copy_template.assert_called_once_with('DUMMY')


if __name__ == '__main__':
    unittest.main()

