import os
import shutil
import lib.clone
import lib.download
import lib.unzip
from command.base_command import BaseCommand
from lib.error import GoogkitError


class SetupCommand(BaseCommand):
    LIBRARY_GIT_REPOS = 'https://code.google.com/p/closure-library/'
    COMPILER_LATEST_ZIP = 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'


    def __init__(self, env):
        super(SetupCommand, self).__init__(env)


    @classmethod
    def needs_config(cls):
        return True


    @classmethod
    def safe_mkdirs(cls, path):
        shutil.rmtree(path, True)
        os.makedirs(path)


    def setup_closure_library(self):
        lib.clone.run(SetupCommand.LIBRARY_GIT_REPOS, self.env.config.library_root())


    def setup_closure_compiler(self):
        SetupCommand.safe_mkdirs('tmp')

        compiler_zip = os.path.join('tmp', 'compiler.zip')
        lib.download.run(SetupCommand.COMPILER_LATEST_ZIP, compiler_zip)

        compiler_root = self.env.config.compiler_root()
        SetupCommand.safe_mkdirs(compiler_root)

        subtool_unzip = os.path.join('tools', 'sub', 'unzip.py')
        lib.unzip.run(compiler_zip, compiler_root)

        shutil.rmtree('tmp')


    def run_internal(self):
        print('Downloading Closure Library...')
        self.setup_closure_library()

        print('Downloading Closure Compiler...')
        self.setup_closure_compiler()
