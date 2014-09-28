import unittest
from pathlib import Path


class FileAssertion(unittest.TestCase):
    def assertExistentFile(self, path):
        is_existent_file = Path(path).exists()

        if not is_existent_file:
            self.print_sibling_paths(path)

        msg = 'Expect a file to be existent, but it not exists: {path}'.format(
            path=str(path))
        self.assertTrue(is_existent_file, msg=msg)


    def assertUnexistentFile(self, path):
        is_existent_file = Path(path).exists()

        if is_existent_file:
            self.print_sibling_paths(path)

        msg = 'Expect a file to be un existent, but it not exists: {path}'.format(
            path=str(path))
        self.assertFalse(is_existent_file, msg=msg)


    def print_sibling_paths(self, path):
        parent = Path(path).parent

        if not parent.exists():
            print('Parent path not exists: {path}'.format(path=str(parent)))
            return

        print('Sibling pathes:')
        for sibling_path in parent.iterdir():
            print(sibling_path)
