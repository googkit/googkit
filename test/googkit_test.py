# Run the following command to test:
#
#     (in /usr/local/googkit)
#     $ python -m {test_module_name}
#
# See also: http://docs.python.org/3.3/library/unittest.html#command-line-interfacejjkkjj
#
# We cannot use unittest.mock on python 2.x!
# Please install the Mock module when you use Python 2.x.
#
#     $ easy_install -U Mock
#
# See also: http://www.voidspace.org.uk/python/mock/#installing

import unittest
import os
import re
from io import BytesIO

if not hasattr(unittest, 'mock'):
    # Python 2.x or 3.2-
    import mock
else:
    # Python 3.3 or later
    import unittest.mock as mock


from googkit import *
from lib.config import Config


class StdoutHook():
    def __init__(self):
        self.orig_stdout = sys.stdout


    def __enter__(self):
        io_base = BytesIO()
        sys.stdout = io_base
        return io_base


    def __exit__(self, *args):
        sys.stdout = self.orig_stdout


class TestGoogkit(unittest.TestCase):
    def setUp(self):
        GLOBAL['ENV'] = { 'GOOGKIT_HOME': '/usr/local/googkit' }


    # print_help {{{
    def test_print_help(self):
        with StdoutHook() as hook:
            hook.write = mock.MagicMock()
            print_help()
            self.assertTrue(hook.write.called)
    # }}}


    # googkit_root {{{
    def test_googkit_root(self):
        self.assertEqual(googkit_root(), '/usr/local/googkit')


    def test_googkit_root_with_no_env(self):
        GLOBAL['ENV'] = {}
        with self.assertRaises(GoogkitError):
            googkit_root()
    # }}}


    # project_root {{{
    def test_project_root_on_grandchild(self):
        os.getcwd = mock.MagicMock()
        os.getcwd.return_value = '/dir1/dir2/dir3/dir4'

        def side_effect(path):
            exists = [
                '/',
                '/dir1',
                '/dir1/dir2',
                '/dir1/dir2/googkit.cfg',
                '/dir1/dir2/dir3',
                '/dir1/dir2/dir3/dir4'
            ]

            return os.path.normpath(path) in exists

        os.path.exists = mock.MagicMock()
        os.path.exists.side_effect = side_effect

        self.assertEqual(project_root(), '/dir1/dir2')


    def test_project_root_on_current(self):
        os.getcwd = mock.MagicMock()
        os.getcwd.return_value = '/dir1/dir2/dir3/dir4'

        def side_effect(path):
            if os.path.normpath(path) == '/dir1/dir2/dir3/dir4/googkit.cfg':
                return True 
            else:
                return False

        os.path.exists = mock.MagicMock()
        os.path.exists.side_effect = side_effect

        self.assertEqual(project_root(), '/dir1/dir2/dir3/dir4')


    def test_project_root_with_on_unrelated(self):
        os.path.exists = mock.MagicMock()
        os.path.exists.return_value = False

        self.assertEqual(project_root(), None)
    # }}}


    # project_config_path {{{
    def test_project_config_path_on_groundchild(self):
        os.getcwd = mock.MagicMock()
        os.getcwd.return_value = '/dir1/dir2/dir3/dir4'

        def side_effect(path):
            exists = [
                '/',
                '/dir1',
                '/dir1/dir2',
                '/dir1/dir2/googkit.cfg',
                '/dir1/dir2/dir3',
                '/dir1/dir2/dir3/dir4'
            ]

            return os.path.normpath(path) in exists

        os.path.exists = mock.MagicMock()
        os.path.exists.side_effect = side_effect

        self.assertEqual(project_config_path(), '/dir1/dir2/googkit.cfg')


    def test_project_config_path_on_current(self):
        os.getcwd = mock.MagicMock()
        os.getcwd.return_value = '/dir1/dir2/dir3/dir4'

        def side_effect(path):
            exists = [
                '/',
                '/dir1',
                '/dir1/dir2',
                '/dir1/dir2/dir3',
                '/dir1/dir2/dir3/dir4',
                '/dir1/dir2/dir3/dir4/googkit.cfg'
            ]

            return os.path.normpath(path) in exists


        os.path.exists = mock.MagicMock()
        os.path.exists.side_effect = side_effect

        self.assertEqual(project_config_path(), '/dir1/dir2/dir3/dir4/googkit.cfg')


    def test_project_config_path_with_on_unrelated(self):
        os.path.exists = mock.MagicMock()
        os.path.exists.return_value = False

        with self.assertRaises(GoogkitError):
            project_config_path()
    # }}}


    # user_config_path {{{
    def test_user_config_path_on_groundchild(self):
        def side_effect_expand_user(path):
            return re.sub(r'~', '/home/user', path)

        os.path.expanduser = mock.MagicMock()
        os.path.expanduser.side_effect = side_effect_expand_user

        os.path.exists = mock.MagicMock()
        os.path.exists.assert_call_with('/home/user/.googkit')

        self.assertEqual(user_config_path(), '/home/user/.googkit')


    def test_user_config_path_with_file_missing(self):
        def side_effect_expand_user(path):
            return re.sub(r'~', '/home/user', path)

        os.path.expanduser = mock.MagicMock()
        os.path.expanduser.side_effect = side_effect_expand_user

        def side_effect_path_exists(path):
            exists = [
                '/',
                '/home',
                '/home/user',
                '/home/user/.googkit']

            return os.path.normpath(path) in exists

        os.path.exists = mock.MagicMock()
        os.path.exists.side_effect = side_effect_path_exists

        self.assertEqual(user_config_path(), '/home/user/.googkit')
    # }}}


    # default_config_path {{{
    def test_default_config_path(self):
        def side_effect_path_exists(path):
            exists = [
                '/',
                '/usr',
                '/usr/local',
                '/usr/local/googkit',
                '/usr/local/googkit/config',
                '/usr/local/googkit/config/default.cfg']

            return os.path.normpath(path) in exists

        os.path.exists = mock.MagicMock()
        os.path.exists.side_effect = side_effect_path_exists

        self.assertEqual(default_config_path(), '/usr/local/googkit/config/default.cfg')


    def test_default_config_path_with_file_missing(self):
        def side_effect_path_exists(path):
            exists = [
                '/',
                '/usr',
                '/usr/local',
                '/usr/local/googkit',
                '/usr/local/googkit/config']

            return os.path.normpath(path) in exists

        os.path.exists = mock.MagicMock()
        os.path.exists.side_effect = side_effect_path_exists

        with self.assertRaises(GoogkitError):
            default_config_path()
    # }}}


    # find_config {{{
    def test_find_config(self):
        os.getcwd = mock.MagicMock()
        os.getcwd.return_value = '/dir1/dir2/dir3/dir4'

        def side_effect_expand_user(path):
            return re.sub(r'~', '/home/user', path)

        os.path.expanduser = mock.MagicMock()
        os.path.expanduser.side_effect = side_effect_expand_user

        def side_effect_path_exists(path):
            exists = [
                '/',
                '/usr',
                '/usr/local',
                '/usr/local/googkit',
                '/usr/local/googkit/config',
                '/usr/local/googkit/config/default.cfg',
                '/dir1',
                '/dir1/dir2',
                '/dir1/dir2/googkit.cfg',
                '/dir1/dir2/dir3',
                '/dir1/dir2/dir3/dir4',
                '/home',
                '/home/user',
                '/home/user/.googkit']

            return os.path.normpath(path) in exists

        os.path.exists = mock.MagicMock()
        os.path.exists.side_effect = side_effect_path_exists

        Config.load = mock.MagicMock()
        find_config()
        Config.load.assert_called_with('/dir1/dir2/googkit.cfg', '/home/user/.googkit', '/usr/local/googkit/config/default.cfg')
    # }}}


if __name__ == '__main__':
    unittest.main()

# vim: fdm=marker
