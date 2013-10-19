import unittest

from test.stub_config import *
from test.stub_environment import StubEnvironment

from googkit.commands.init import InitCommand
from googkit.compat.unittest import mock
from googkit.lib.error import GoogkitError


class TestInitCommand(unittest.TestCase):
    def setUp(self):
        self.env = StubEnvironment()
        self.env.config = StubConfig()
        self.cmd = InitCommand(self.env)

    def test_needs_project_config(self):
        self.assertFalse(InitCommand.needs_project_config())

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
