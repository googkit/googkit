import os
import shutil
import tempfile
import unittest
import googkit.lib.file


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
