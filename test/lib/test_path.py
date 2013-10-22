import unittest
import os
import re
import googkit.lib.path
from googkit.compat.unittest import mock
from googkit.lib.error import GoogkitError


def is_path_equal(a, b):
    return os.path.abspath(a) == os.path.abspath(b)


class TestPath(unittest.TestCase):
    def assertPathEqual(self, actual, expected):
        self.assertEqual(os.path.abspath(actual), os.path.abspath(expected))

    def test_project_root_on_grandchild(self):
        def stub_exists(path):
            exists = [os.path.abspath(exist) for exist in [
                '/',
                '/dir1',
                '/dir1/dir2',
                '/dir1/dir2/googkit.cfg',
                '/dir1/dir2/dir3',
                '/dir1/dir2/dir3/dir4',
            ]]

            return os.path.abspath(path) in exists

        cwd = os.path.normcase('/dir1/dir2/dir3/dir4')
        with mock.patch('os.path.exists', side_effect=stub_exists):
            self.assertPathEqual(
                googkit.lib.path.project_root(cwd),
                '/dir1/dir2')

    def test_project_root_on_current(self):
        def stub_exists(path):
            exists = [os.path.abspath(exist) for exist in [
                '/',
                '/dir1',
                '/dir1/dir2',
                '/dir1/dir2/dir3',
                '/dir1/dir2/dir3/dir4',
                '/dir1/dir2/dir3/dir4/googkit.cfg',
            ]]

            return os.path.abspath(path) in exists

        cwd = os.path.normcase('/dir1/dir2/dir3/dir4')
        with mock.patch('os.path.exists', side_effect=stub_exists):
            self.assertPathEqual(
                googkit.lib.path.project_root(cwd),
                '/dir1/dir2/dir3/dir4')

    def test_project_config(self):
        def stub_exists(path):
            if is_path_equal(path, '/dir1/dir2/googkit.cfg'):
                return True
            else:
                return False

        cwd = os.path.normcase('/dir1/dir2/dir3/dir4')
        dummy_project_root = os.path.normcase('/dir1/dir2')
        with mock.patch('os.path.exists', side_effect=stub_exists), \
                mock.patch('googkit.lib.path.project_root', return_value=dummy_project_root):
            self.assertPathEqual(
                googkit.lib.path.project_config(cwd),
                '/dir1/dir2/googkit.cfg')

    def test_user_config_on_groundchild(self):
        def stub_expanduser(path):
            return re.sub(r'~', '/home/user', path)

        with mock.patch('os.path.expanduser', side_effect=stub_expanduser), \
                mock.patch('os.path.exists'):

            self.assertPathEqual(
                googkit.lib.path.user_config(),
                '/home/user/.googkit')

    def test_user_config_with_file_missing(self):
        def stub_expanduser(path):
            return re.sub(r'~', '/home/user', path)

        def stub_exists(path):
            exists = [os.path.abspath(exist) for exist in [
                '/',
                '/home',
                '/home/user',
                '/home/user/.googkit']]

            return os.path.abspath(path) in exists

        with mock.patch('os.path.expanduser', side_effect=stub_expanduser), \
                mock.patch('os.path.exists', side_effect=stub_exists):
            self.assertPathEqual(googkit.lib.path.user_config(), '/home/user/.googkit')

    def test_default_config(self):
        def stub_exists(path):
            exists = [os.path.abspath(exist) for exist in [
                '/',
                '/dummy',
                '/dummy/usr',
                '/dummy/usr/local',
                '/dummy/usr/local/googkit',
                '/dummy/usr/local/googkit/etc',
                '/dummy/usr/local/googkit/etc/default.cfg']]

            return os.path.abspath(path) in exists

        dummy_googkit_root = os.path.normcase('/dummy/usr/local/googkit')

        with mock.patch('os.path.exists', side_effect=stub_exists), \
                mock.patch('googkit.lib.path.googkit_root', return_value=dummy_googkit_root):
            self.assertPathEqual(
                googkit.lib.path.default_config(),
                '/dummy/usr/local/googkit/etc/default.cfg')

    def test_googkit_root(self):
        dummy_path = os.path.normcase('/dummy/googkit/googkit/lib/path.py')

        with mock.patch('googkit.lib.path.__file__', new=dummy_path):
            self.assertPathEqual(googkit.lib.path.googkit_root(), '/dummy/googkit')

    def test_plugin(self):
        def stub_isdir(path):
            return is_path_equal(path, '/dummy/usr/local/googkit/googkit/plugins')

        dummy_googkit_root = os.path.normcase('/dummy/usr/local/googkit')

        with mock.patch('googkit.lib.path.googkit_root', return_value=dummy_googkit_root), \
                mock.patch('os.path.isdir', side_effect=stub_isdir):
            self.assertPathEqual(
                googkit.lib.path.plugin(),
                '/dummy/usr/local/googkit/googkit/plugins')

    def test_plugin_with_directory_missing(self):
        dummy_googkit_root = os.path.normcase('/dummy/usr/local/googkit')
        with mock.patch('googkit.lib.path.googkit_root', return_value=dummy_googkit_root), \
                mock.patch('os.path.isdir', return_value=False):
            with self.assertRaises(GoogkitError):
                self.assertPathEqual(
                    googkit.lib.path.plugin(),
                    '/dummy/usr/local/googkit/plugins')

    def test_template(self):
        def stub_isdir(path):
            return is_path_equal(path, '/dummy/usr/local/googkit/etc/template')

        dummy_googkit_root = os.path.normcase('/dummy/usr/local/googkit')
        with mock.patch('googkit.lib.path.googkit_root', return_value=dummy_googkit_root), \
                mock.patch('os.path.isdir', side_effect=stub_isdir):
            self.assertPathEqual(
                googkit.lib.path.template(),
                '/dummy/usr/local/googkit/etc/template')

    def test_template_with_directory_missing(self):
        dummy_googkit_root = os.path.normcase('/dummy/usr/local/googkit')
        with mock.patch('googkit.lib.path.googkit_root', return_value=dummy_googkit_root), \
                mock.patch('os.path.isdir', return_value=False):
            with self.assertRaises(GoogkitError):
                self.assertPathEqual(
                    googkit.lib.path.template(),
                    '/dummy/usr/local/googkit/etc/template')
