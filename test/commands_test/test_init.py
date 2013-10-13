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

from googkit.lib.error import GoogkitError
from googkit.cmds.init import InitCommand

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
        template_dir = '/tmp/dummy'

        def listdir(path):
            if path == dst_path:
                return ['dummy1', 'dummy2']
            elif path == template_dir:
                return ['dummy3']
            else:
                self.failed('Unexpected path: ' + path)

        with mock.patch('os.listdir', side_effect=listdir) as mock_listdir, \
                mock.patch('distutils.dir_util.copy_tree') as mock_copytree, \
                mock.patch('googkit.lib.path.template', return_value=template_dir):
            self.cmd.copy_template(dst_path)

        mock_copytree.assert_called_once_with(template_dir, dst_path)


    def test_copy_templates_with_conflict(self):
        dst_path = '/tmp/foo/bar'
        template_dir = '/tmp/dummy'

        def listdir(path):
            if path == dst_path:
                return ['dummy1', 'dummy2', 'conflicted']
            elif path == template_dir:
                return ['dummy3', 'conflicted']
            else:
                self.failed('Unexpected path: ' + path)

        with mock.patch('os.listdir', side_effect=listdir) as mock_listdir, \
                mock.patch('distutils.dir_util.copy_tree'), \
                mock.patch('googkit.lib.path.template', return_value=template_dir):
            with self.assertRaises(GoogkitError):
                self.cmd.copy_template(dst_path)


    def test_run_internal(self):
        self.cmd.copy_template = mock.MagicMock()

        with mock.patch('os.getcwd', return_value='dummy'):
            self.cmd.run_internal()

        self.cmd.copy_template.assert_called_once_with('dummy')


if __name__ == '__main__':
    unittest.main()
