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

try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock

import os
import googkit.lib.plugin
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
        def is_exists(path):
            exists = [
                '/dummy/plugins/dummy1',
                '/dummy/plugins/dummy1/__init__.py',
                '/dummy/plugins/dummy1/command.py',
                '/dummy/plugins/dummy2',
                '/dummy/plugins/dummy2/__init__.py',
                '/dummy/plugins/dummy2/command.py',
                '/dummy/plugins/__init__.py'
            ]
            return os.path.abspath(path) in exists

        def is_dir(path):
            dirs = [
                '/dummy/plugins/dummy1',
                '/dummy/plugins/dummy2'
            ]
            return os.path.abspath(path) in dirs

        mock_tree = mock.MagicMock()
        mock_module = StubPlugin()
        mock_module.register = mock.MagicMock()

        with mock.patch('os.listdir', return_value=['dummy1', 'dummy2']), \
                mock.patch('googkit.lib.path.plugin', return_value='/dummy/plugins'), \
                mock.patch('os.path.exists', side_effect=is_exists), \
                mock.patch('os.path.isdir', side_effect=is_dir), \
                mock.patch('googkit.lib.plugin.__import__', create=True, return_value=mock_module) as mock_import:
            googkit.lib.plugin.load(mock_tree)

        mock_import.assert_any_call('plugins.dummy1.command', fromlist=['command'])
        mock_import.assert_any_call('plugins.dummy2.command', fromlist=['command'])
        self.assertEqual(mock_import.call_count, 2)

        mock_module.register.assert_any_call(mock_tree)
        self.assertEqual(mock_module.register.call_count, 2)

    def test_load_with_no_plugins(self):
        def is_exists(path):
            exists = [
                '/dummy/plugins/__init__.py'
            ]
            return os.path.abspath(path) in exists

        mock_tree = mock.MagicMock()
        mock_module = StubPlugin()
        mock_module.register = mock.MagicMock()

        with mock.patch('os.listdir', return_value=[]), \
                mock.patch('googkit.lib.path.plugin', return_value='/dummy/plugins'), \
                mock.patch('os.path.exists', side_effect=is_exists), \
                mock.patch('os.path.isdir', return_value=False), \
                mock.patch('googkit.lib.plugin.__import__', create=True, return_value=mock_module) as mock_import:
            googkit.lib.plugin.load(mock_tree)

        self.assertFalse(mock_import.called)

    def test_load_with_invalid_plugin(self):
        def is_exists(path):
            exists = [
                '/dummy/plugins/invalid1',
                '/dummy/plugins/invalid1/__init__.py',
                '/dummy/plugins/invalid1/command.py',
                '/dummy/plugins/invalid2',
                '/dummy/plugins/invalid2/__init__.py',
                '/dummy/plugins/invalid2/command.py',
                '/dummy/plugins/__init__.py'
            ]
            return os.path.abspath(path) in exists

        def is_dir(path):
            dirs = [
                '/dummy/plugins/invalid1',
                '/dummy/plugins/invalid2'
            ]
            return os.path.abspath(path) in dirs

        mock_tree = mock.MagicMock()
        mock_module = StubInvalidPlugin()

        with mock.patch('os.listdir', return_value=['invalid1', 'invalid2']), \
                mock.patch('googkit.lib.path.plugin', return_value='/dummy/plugins'), \
                mock.patch('os.path.exists', side_effect=is_exists), \
                mock.patch('os.path.isdir', side_effect=is_dir), \
                mock.patch('googkit.lib.plugin.__import__', create=True, return_value=mock_module):
            with self.assertRaises(GoogkitError):
                googkit.lib.plugin.load(mock_tree)

    def test_load_without_init_file(self):
        def is_exists(path):
            exists = [
                '/dummy/plugins/no_init1',
                '/dummy/plugins/no_init1/command.py',
                '/dummy/plugins/no_init2',
                '/dummy/plugins/no_init2/__init__.py',
                '/dummy/plugins/no_init2/command.py',
                '/dummy/plugins/__init__.py'
            ]
            return os.path.abspath(path) in exists

        def is_dir(path):
            dirs = [
                '/dummy/plugins/no_init1',
                '/dummy/plugins/no_init2'
            ]
            return os.path.abspath(path) in dirs

        mock_tree = mock.MagicMock()
        mock_module = StubPlugin()
        mock_module.register = mock.MagicMock()

        with mock.patch('os.listdir', return_value=['no_init1', 'no_init2']), \
                mock.patch('googkit.lib.path.plugin', return_value='/dummy/plugins'), \
                mock.patch('os.path.exists', side_effect=is_exists), \
                mock.patch('os.path.isdir', side_effect=is_dir), \
                mock.patch('googkit.lib.plugin.__import__', create=True, return_value=mock_module) as mock_import:
            with self.assertRaises(GoogkitError):
                googkit.lib.plugin.load(mock_tree)

        self.assertFalse(mock_import.called)
