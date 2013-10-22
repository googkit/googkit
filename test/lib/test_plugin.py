import unittest
import os

import googkit.lib.plugin
from googkit.compat.unittest import mock
from googkit.lib.error import GoogkitError


class StubPlugin(object):
    def __init__(self):
        pass

    def register(self, tree):
        pass


class StubInvalidPlugin(object):
    def __init__(self):
        pass


class TestPlugin(unittest.TestCase):
    def test_load_with_two_plugins(self):
        def stub_exists(path):
            exists = [os.path.abspath(path) for path in [
                '/dummy/plugins/dummy1',
                '/dummy/plugins/dummy1/__init__.py',
                '/dummy/plugins/dummy1/command.py',
                '/dummy/plugins/dummy2',
                '/dummy/plugins/dummy2/__init__.py',
                '/dummy/plugins/dummy2/command.py',
                '/dummy/plugins/__init__.py'
            ]]
            return os.path.abspath(path) in exists

        def stub_isdir(path):
            dirs = [os.path.abspath(path) for path in [
                '/dummy/plugins/dummy1',
                '/dummy/plugins/dummy2'
            ]]
            return os.path.abspath(path) in dirs

        mock_tree = mock.MagicMock()
        mock_module = StubPlugin()
        mock_module.register = mock.MagicMock()
        dummy_plugin_dir = os.path.normcase('/dummy/plugins')

        with mock.patch('os.listdir', return_value=['dummy1', 'dummy2']), \
                mock.patch('googkit.lib.path.plugin', return_value=dummy_plugin_dir), \
                mock.patch('os.path.exists', side_effect=stub_exists), \
                mock.patch('os.path.isdir', side_effect=stub_isdir), \
                mock.patch('googkit.lib.plugin.__import__', create=True, return_value=mock_module) as mock_import:
            googkit.lib.plugin.load(mock_tree)

        mock_import.assert_any_call('plugins.dummy1.command', fromlist=['command'])
        mock_import.assert_any_call('plugins.dummy2.command', fromlist=['command'])
        self.assertEqual(mock_import.call_count, 2)

        mock_module.register.assert_any_call(mock_tree)
        self.assertEqual(mock_module.register.call_count, 2)

    def test_load_with_no_plugins(self):
        def stub_exists(path):
            exists = [os.path.abspath(path) for path in [
                '/dummy/plugins/__init__.py'
            ]]
            return os.path.abspath(path) in exists

        mock_tree = mock.MagicMock()
        mock_module = StubPlugin()
        mock_module.register = mock.MagicMock()
        dummy_plugin_dir = os.path.normcase('/dummy/plugins')

        with mock.patch('os.listdir', return_value=[]), \
                mock.patch('googkit.lib.path.plugin', return_value=dummy_plugin_dir), \
                mock.patch('os.path.exists', side_effect=stub_exists), \
                mock.patch('os.path.isdir', return_value=False), \
                mock.patch('googkit.lib.plugin.__import__', create=True, return_value=mock_module) as mock_import:
            googkit.lib.plugin.load(mock_tree)

        self.assertFalse(mock_import.called)

    def test_load_with_invalid_plugin(self):
        def stub_exists(path):
            exists = [os.path.abspath(path) for path in [
                '/dummy/plugins/invalid1',
                '/dummy/plugins/invalid1/__init__.py',
                '/dummy/plugins/invalid1/command.py',
                '/dummy/plugins/invalid2',
                '/dummy/plugins/invalid2/__init__.py',
                '/dummy/plugins/invalid2/command.py',
                '/dummy/plugins/__init__.py'
            ]]
            return os.path.abspath(path) in exists

        def stub_isdir(path):
            dirs = [os.path.abspath(path) for path in [
                '/dummy/plugins/invalid1',
                '/dummy/plugins/invalid2'
            ]]
            return os.path.abspath(path) in dirs

        mock_tree = mock.MagicMock()
        mock_module = StubInvalidPlugin()
        dummy_plugin_dir = os.path.normcase('/dummy/plugins')

        with mock.patch('os.listdir', return_value=['invalid1', 'invalid2']), \
                mock.patch('googkit.lib.path.plugin', return_value=dummy_plugin_dir), \
                mock.patch('os.path.exists', side_effect=stub_exists), \
                mock.patch('os.path.isdir', side_effect=stub_isdir), \
                mock.patch('googkit.lib.plugin.__import__', create=True, return_value=mock_module):
            with self.assertRaises(GoogkitError):
                googkit.lib.plugin.load(mock_tree)

    def test_load_without_init_file(self):
        def stub_exists(path):
            exists = [os.path.abspath(path) for path in [
                '/dummy/plugins/no_init1',
                '/dummy/plugins/no_init1/command.py',
                '/dummy/plugins/no_init2',
                '/dummy/plugins/no_init2/__init__.py',
                '/dummy/plugins/no_init2/command.py',
                '/dummy/plugins/__init__.py'
            ]]
            return os.path.abspath(path) in exists

        def stub_isdir(path):
            dirs = [os.path.abspath(path) for path in [
                '/dummy/plugins/no_init1',
                '/dummy/plugins/no_init2'
            ]]
            return os.path.abspath(path) in dirs

        mock_tree = mock.MagicMock()
        mock_module = StubPlugin()
        mock_module.register = mock.MagicMock()
        dummy_plugin_dir = os.path.normcase('/dummy/plugins')

        with mock.patch('os.listdir', return_value=['no_init1', 'no_init2']), \
                mock.patch('googkit.lib.path.plugin', return_value=dummy_plugin_dir), \
                mock.patch('os.path.exists', side_effect=stub_exists), \
                mock.patch('os.path.isdir', side_effect=stub_isdir), \
                mock.patch('googkit.lib.plugin.__import__', create=True, return_value=mock_module):
            # should not raise any error
            googkit.lib.plugin.load(mock_tree)
