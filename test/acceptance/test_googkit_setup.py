import unittest
import mock

import shutil
from pathlib import Path

import test.cwd
from test.asserting.file_assertion import FileAssertion

FIXTURE_PATH = Path('test', 'acceptance', 'fixture', 'setup')
SAMPLE_PROJECT_NAME = 'sample_project'
SAMPLE_PROJECT_PATH = Path(FIXTURE_PATH, SAMPLE_PROJECT_NAME)

SAMPLE_PROJECT_TEMPLATE_PATH = Path(FIXTURE_PATH, 'sample_project_template')


class AcceptanceTestGoogkitSetup(FileAssertion, unittest.TestCase):
    def setUp(self):
        self.rm_project_dir_if_exists()
        self.create_project_dir_by_template()


    def tearDown(self):
        self.rm_project_dir_if_exists()


    def test_execute_googkit_setup(self):
        """ This test case simulates that user run `googkit init` in just his
        project directiry to initialize the project.

        $ cd path/to/sample_project
        $ googkit init
        $ googkit setup

        But this test use fixture repository as a closure library, and closure
        compiler. See https://github.com/googkit/googkit-test-repo .
        """

        # This argv will be used as a sys.argv for this command execution
        argv = ['path/to/googkit/googkt.py', 'setup']

        # Mock sys.argv to simulate run `googkit setup`, and simulate the user
        # is on the sample project root directory.
        with test.cwd.chdir(SAMPLE_PROJECT_PATH), \
                mock.patch('sys.argv', argv):

            import googkit
            googkit.main()

        closure_tools_path = Path(SAMPLE_PROJECT_PATH, 'closure')
        closure_compiler_path = Path(closure_tools_path, 'compiler')
        closure_library_path = Path(closure_tools_path, 'library')

        self.assertExistentFile(closure_compiler_path)
        self.assertExistentFile(closure_library_path)


    def create_project_dir_by_template(self):
        # copytree requires string path
        sample_project_path_str = str(SAMPLE_PROJECT_PATH)
        sample_project_template_path_str = str(SAMPLE_PROJECT_TEMPLATE_PATH)

        shutil.copytree(sample_project_template_path_str,
                        sample_project_path_str)


    def rm_project_dir_if_exists(self):
        if not SAMPLE_PROJECT_PATH.exists():
            return

        # rmtree requires string path
        sample_project_path_str = str(SAMPLE_PROJECT_PATH)
        shutil.rmtree(sample_project_path_str)


if __name__ == '__main__':
    unittest.main()
