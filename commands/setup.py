import os
import os.path
import shutil
import lib.clone
import lib.download
import lib.unzip
from lib.error import GoogkitError


class SetupCommand(object):
    LIBRARY_GIT_REPOS = 'https://code.google.com/p/closure-library/'
    COMPILER_LATEST_ZIP = 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'


    def __init__(self, env):
        self.env = env


    @classmethod
    def needs_config(cls):
        return True


    def setup_closure_library(self):
        lib.clone.run(SetupCommand.LIBRARY_GIT_REPOS, self.env.config.library_root())


    @classmethod
    def safe_mkdirs(cls, path):
        shutil.rmtree(path, True)
        os.makedirs(path)


    def setup_closure_compiler(self):
        SetupCommand.safe_mkdirs('tmp')

        compiler_zip = os.path.join('tmp', 'compiler.zip')
        lib.download.run(SetupCommand.COMPILER_LATEST_ZIP, compiler_zip)

        compiler_root = self.env.config.compiler_root()
        SetupCommand.safe_mkdirs(compiler_root)

        subtool_unzip = os.path.join('tools', 'sub', 'unzip.py')
        lib.unzip.run(compiler_zip, compiler_root)

        shutil.rmtree('tmp')


    def run(self):
        if self.env.config is None:
            raise GoogkitError('No config file found.')

        print('Downloading Closure Library...')
        self.setup_closure_library()

        print('Downloading Closure Compiler...')
        self.setup_closure_compiler()

        print('Completed.')
