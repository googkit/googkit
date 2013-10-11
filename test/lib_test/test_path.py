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

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock


import lib.path
from lib.error import GoogkitError
from test.stub_stdout import StubStdout


class TestPath(unittest.TestCase):
    def test_project_root_on_grandchild(self):
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

        with mock.patch('os.getcwd', return_value = '/dir1/dir2/dir3/dir4'), \
                mock.patch('os.path.exists', side_effect = side_effect):
            self.assertEqual(lib.path.project_root(), '/dir1/dir2')


    def test_project_root_on_current(self):
        def side_effect(path):
            if os.path.normpath(path) == '/dir1/dir2/dir3/dir4/googkit.cfg':
                return True 
            else:
                return False

        with mock.patch('os.getcwd', return_value = '/dir1/dir2/dir3/dir4'), \
                mock.patch('os.path.exists', side_effect = side_effect):
            self.assertEqual(lib.path.project_root(), '/dir1/dir2/dir3/dir4')


    def test_project_root_with_on_unrelated(self):
        with mock.patch('os.path.exists', return_value = False):
            self.assertEqual(lib.path.project_root(), None)


    def test_project_config_on_groundchild(self):
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

        with mock.patch('os.getcwd', return_value = '/dir1/dir2/dir3/dir4'), \
                mock.patch('os.path.exists', side_effect = side_effect):
            self.assertEqual(lib.path.project_config(), '/dir1/dir2/googkit.cfg')


    def test_project_config_on_current(self):
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

        with mock.patch('os.getcwd', return_value = '/dir1/dir2/dir3/dir4'), \
                mock.patch('os.path.exists', side_effect = side_effect):
            self.assertEqual(lib.path.project_config(), '/dir1/dir2/dir3/dir4/googkit.cfg')


    def test_project_config_with_on_unrelated(self):
        with mock.patch('os.path.exists', return_value = False):
            with self.assertRaises(GoogkitError):
                lib.path.project_config()


    def test_user_config_on_groundchild(self):
        def side_effect_expand_user(path):
            return re.sub(r'~', '/home/user', path)

        with mock.patch('os.path.expanduser', side_effect = side_effect_expand_user), \
                mock.patch('os.path.exists'):

            self.assertEqual(lib.path.user_config(), '/home/user/.googkit')


    def test_user_config_with_file_missing(self):
        def side_effect_expand_user(path):
            return re.sub(r'~', '/home/user', path)

        def side_effect_exists(path):
            exists = [
                '/',
                '/home',
                '/home/user',
                '/home/user/.googkit']

            return os.path.normpath(path) in exists

        with mock.patch('os.path.expanduser', side_effect = side_effect_expand_user), \
                mock.patch('os.path.exists', side_effect = side_effect_exists):
            self.assertEqual(lib.path.user_config(), '/home/user/.googkit')


    def test_default_config(self):
        def side_effect_exists(path):
            exists = [
                '/',
                '/dummy',
                '/dummy/usr',
                '/dummy/usr/local',
                '/dummy/usr/local/googkit',
                '/dummy/usr/local/googkit/config',
                '/dummy/usr/local/googkit/config/default.cfg']

            return os.path.normpath(path) in exists

        with mock.patch('os.path.exists', side_effect = side_effect_exists), \
                mock.patch('lib.path.googkit_root', return_value = '/dummy/usr/local/googkit'):
            self.assertEqual(lib.path.default_config(), '/dummy/usr/local/googkit/config/default.cfg')


    def test_default_config_with_file_missing(self):
        def side_effect_exists(path):
            exists = [
                '/',
                '/dummy',
                '/dummy/usr',
                '/dummy/usr/local',
                '/dummy/usr/local/googkit',
                '/dummy/usr/local/googkit/config']

            return os.path.normpath(path) in exists

        with mock.patch('os.path.exists', side_effect = side_effect_exists), \
                mock.patch('lib.path.googkit_root', return_value = '/dummy/usr/local/googkit'):
            with self.assertRaises(GoogkitError):
                lib.path.default_config()
