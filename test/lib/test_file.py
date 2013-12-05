import os
import shutil
import tempfile
import unittest
import googkit.lib.file
from googkit.compat.unittest import mock


class TestFile(unittest.TestCase):
    def _build_structure(self, base_dir, structure):
        """Build a directory structure for testing.
            self._build_structure('/foobar', {
                'dir': {
                    'file-b': True
                },
                'file-a'
            })
        builds:
            /
            `-- foobar/
                |-- dir/
                |   `-- file-b
                `-- file-a
        """
        for key, value in structure.items():
            if isinstance(value, dict):
                newdir = os.path.join(base_dir, key)
                os.mkdir(newdir)
                self._build_structure(
                    newdir,
                    value)
            else:
                newfile = os.path.join(base_dir, key)
                with open(newfile, 'w') as f:
                    f.write(str(value))

    def test_copytree(self):
        src_dir = tempfile.mkdtemp()
        self._build_structure(src_dir, {
            'sub': {
                'subsub': {
                    'subsubfile': True
                },
                'subfile': True
            },
            'file': True
        })

        dst_dir = tempfile.mkdtemp()
        self._build_structure(dst_dir, {
            'oldfile': True
        })

        # copytree to non-empty dir should not raise an error
        googkit.lib.file.copytree(src_dir, dst_dir)

        self.assertTrue(
            os.path.exists(os.path.join(dst_dir, 'sub', 'subfile')),
            'A file in subfolder should exist')
        self.assertTrue(
            os.path.exists(os.path.join(dst_dir, 'sub', 'subsub', 'subsubfile')),
            'A file in subsubfolder should exist')
        self.assertTrue(
            os.path.exists(os.path.join(dst_dir, 'oldfile')),
            'Existing file should be kept')

        shutil.rmtree(src_dir)
        shutil.rmtree(dst_dir)

    def test_copytree_with_ignore(self):
        src_dir = tempfile.mkdtemp()
        self._build_structure(src_dir, {
            'sub': {
                'subsub': {
                    'subsubfile': True
                },
                'subfile': True
            },
            'file': True
        })

        dst_dir = tempfile.mkdtemp()

        def ignore(target_dir, files):
            # Ignores directory 'sub'
            return ['sub'] if target_dir == src_dir else []

        googkit.lib.file.copytree(src_dir, dst_dir, ignore=ignore)

        self.assertFalse(
            os.path.exists(os.path.join(dst_dir, 'sub')),
            'Ignored directory should not exist')
        self.assertFalse(
            os.path.exists(os.path.join(dst_dir, 'sub', 'subsub')),
            'Contents in ignored directory should not exist')
        self.assertTrue(
            os.path.exists(os.path.join(dst_dir, 'file')),
            'Contents that is not ignored should exist')

        shutil.rmtree(src_dir)
        shutil.rmtree(dst_dir)

    def test_executable(self):
        with mock.patch('os.path.isfile', return_value=True), \
                mock.patch('os.access', return_value=True):
            self.assertTrue(
                googkit.lib.file.executable('/foo/bar'),
                'Executable file should be executable')

        with mock.patch('os.path.isfile', return_value=False):
            self.assertFalse(
                googkit.lib.file.executable('/foo/bar'),
                'Non-existent file should not be executable')

    def test_which(self):
        os_pathsep = ':'
        os_environ = {
            'PATH': os_pathsep.join([
                '/usr/local/bin',
                '/usr/bin'
            ])
        }

        def os_path_exists(path):
            return os.path.abspath(path) in [
                '/usr',
                '/usr/bin/cmd0',
                '/usr/local',
                '/usr/local/bin',
                '/usr/local/bin/cmd1',
            ]

        def executable(path):
            return path in [
                '/usr/bin/cmd0',
                '/usr/local/bin/cmd1',
            ]

        with mock.patch('os.environ', new=os_environ), \
                mock.patch('os.pathsep', new=os_pathsep), \
                mock.patch('os.path.exists', side_effect=os_path_exists), \
                mock.patch('googkit.lib.file.executable', side_effect=executable):
            self.assertTrue(
                googkit.lib.file.which('cmd0'))
            self.assertFalse(
                googkit.lib.file.which('bluerose'))
