import unittest
import mock

import shutil
from pathlib import Path

from test.asserting.file_assertion import FileAssertion
import test.cwd


FIXTURE_PATH = Path('test', 'acceptance', 'fixture', 'init')
SAMPLE_PROJECT_NAME = 'sample_project'
SAMPLE_PROJECT_PATH = Path(FIXTURE_PATH, SAMPLE_PROJECT_NAME)


class AcceptanceTestGoogkitInit(FileAssertion, unittest.TestCase):
    def setUp(self):
        self.rm_project_dir_if_exists()
        self.mk_project_dir()


    def tearDown(self):
        self.rm_project_dir_if_exists()


    def test_execute_googkit_init(self):
        """ This test case simulates that user run `googkit init` in just his
        project directiry to initialize the project.

        $ mkdir -p path/to/sample_project
        $ cd path/to/sample_project
        $ googkit init
        """

        # This argv will be used as a sys.argv for this command execution
        argv = ['path/to/googkit/googkt.py', 'init']

        # Mock sys.argv to simulate run `googkit init`, and simulate the user
        # is on the sample project root directory.
        with test.cwd.chdir(SAMPLE_PROJECT_PATH), \
                mock.patch('sys.argv', argv):

            import googkit
            googkit.main()

        googkit_cfg_path = Path(SAMPLE_PROJECT_PATH, 'googkit.cfg')
        self.assertExistentFile(googkit_cfg_path)


    def rm_project_dir_if_exists(self):
        if not SAMPLE_PROJECT_PATH.exists():
            return

        # rmtree requires string path
        sample_project_path_str = str(SAMPLE_PROJECT_PATH)
        shutil.rmtree(sample_project_path_str)


    def mk_project_dir(self):
        SAMPLE_PROJECT_PATH.mkdir(parents=True)


if __name__ == '__main__':
    unittest.main()
