import unittest
import os
import re

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock


import googkit.lib.path
from googkit.lib.error import GoogkitError


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

        with mock.patch('os.path.exists', side_effect=side_effect):
            self.assertEqual(
                googkit.lib.path.project_root('/dir1/dir2/dir3/dir4'),
                '/dir1/dir2')

    def test_project_root_on_current(self):
        def side_effect(path):
            if os.path.normpath(path) == '/dir1/dir2/dir3/dir4/googkit.cfg':
                return True
            else:
                return False

        with mock.patch('os.path.exists', side_effect=side_effect):
            self.assertEqual(
                googkit.lib.path.project_root('/dir1/dir2/dir3/dir4'),
                '/dir1/dir2/dir3/dir4')

    def test_project_root_with_on_unrelated(self):
        with mock.patch('os.path.exists', return_value=False):
            self.assertEqual(googkit.lib.path.project_root('/cwd'), None)

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

        with mock.patch('os.path.exists', side_effect=side_effect):
            self.assertEqual(
                googkit.lib.path.project_config('/dir1/dir2/dir3/dir4'),
                '/dir1/dir2/googkit.cfg')

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

        with mock.patch('os.path.exists', side_effect=side_effect):
            self.assertEqual(
                googkit.lib.path.project_config('/dir1/dir2/dir3/dir4'),
                '/dir1/dir2/dir3/dir4/googkit.cfg')

    def test_project_config_with_on_unrelated(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(GoogkitError):
                googkit.lib.path.project_config('/cwd')

    def test_user_config_on_groundchild(self):
        def side_effect_expand_user(path):
            return re.sub(r'~', '/home/user', path)

        with mock.patch('os.path.expanduser', side_effect=side_effect_expand_user), \
                mock.patch('os.path.exists'):

            self.assertEqual(googkit.lib.path.user_config(), '/home/user/.googkit')

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

        with mock.patch('os.path.expanduser', side_effect=side_effect_expand_user), \
                mock.patch('os.path.exists', side_effect=side_effect_exists):
            self.assertEqual(googkit.lib.path.user_config(), '/home/user/.googkit')

    def test_default_config(self):
        def side_effect_exists(path):
            exists = [
                '/',
                '/dummy',
                '/dummy/usr',
                '/dummy/usr/local',
                '/dummy/usr/local/googkit',
                '/dummy/usr/local/googkit/etc',
                '/dummy/usr/local/googkit/etc/default.cfg']

            return os.path.normpath(path) in exists

        with mock.patch('os.path.exists', side_effect=side_effect_exists), \
                mock.patch('googkit.lib.path.googkit_root', return_value='/dummy/usr/local/googkit'):
            self.assertEqual(googkit.lib.path.default_config(), '/dummy/usr/local/googkit/etc/default.cfg')

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

        with mock.patch('os.path.exists', side_effect=side_effect_exists), \
                mock.patch('googkit.lib.path.googkit_root', return_value='/dummy/usr/local/googkit'):
            with self.assertRaises(GoogkitError):
                googkit.lib.path.default_config()

    def test_googkit_root(self):
        with mock.patch('googkit.lib.path.__file__', new='/dummy/googkit/googkit/lib/path.py'):
            self.assertEqual(googkit.lib.path.googkit_root(), '/dummy/googkit')

    def test_plugin(self):
        def side_effect(path):
            return os.path.abspath(path) == '/dummy/usr/local/googkit/googkit/plugins'

        with mock.patch('googkit.lib.path.googkit_root', return_value='/dummy/usr/local/googkit'), \
                mock.patch('os.path.isdir', side_effect=side_effect):
            self.assertEqual(googkit.lib.path.plugin(), '/dummy/usr/local/googkit/googkit/plugins')

    def test_plugin_with_directory_missing(self):
        with mock.patch('googkit.lib.path.googkit_root', return_value='/dummy/usr/local/googkit'), \
                mock.patch('os.path.isdir', return_value=False):
            with self.assertRaises(GoogkitError):
                self.assertEqual(googkit.lib.path.plugin(), '/dummy/usr/local/googkit/plugins')

    def test_template(self):
        def side_effect(path):
            return os.path.abspath(path) == '/dummy/usr/local/googkit/etc/template'

        with mock.patch('googkit.lib.path.googkit_root', return_value='/dummy/usr/local/googkit'), \
                mock.patch('os.path.isdir', side_effect=side_effect):
            self.assertEqual(googkit.lib.path.template(), '/dummy/usr/local/googkit/etc/template')

    def test_template_with_directory_missing(self):
        with mock.patch('googkit.lib.path.googkit_root', return_value='/dummy/usr/local/googkit'), \
                mock.patch('os.path.isdir', return_value=False):
            with self.assertRaises(GoogkitError):
                self.assertEqual(googkit.lib.path.template(), '/dummy/usr/local/googkit/etc/template')
