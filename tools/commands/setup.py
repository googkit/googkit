import os
import os.path
import shutil
import lib.clone
import lib.download
import lib.unzip


class SetupCommand(object):
    LIBRARY_GIT_REPOS = 'https://code.google.com/p/closure-library/'
    COMPILER_LATEST_ZIP = 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'


    def __init__(self, config):
        self.config = config


    def setup_closure_library(self):
        lib.clone.run(SetupCommand.LIBRARY_GIT_REPOS, self.config.library_root())


    def setup_closure_compiler(self):
        os.makedirs('tmp')

        compiler_zip = os.path.join('tmp', 'compiler.zip')
        lib.download.run(SetupCommand.COMPILER_LATEST_ZIP, compiler_zip)

        compiler_root = self.config.compiler_root()
        os.makedirs(compiler_root)

        subtool_unzip = os.path.join('tools', 'sub', 'unzip.py')
        lib.unzip.run(compiler_zip, compiler_root)

        shutil.rmtree('tmp')


    def run(self):
        print 'Downloading Closure Library...'
        self.setup_closure_library()

        print 'Downloading Closure Compiler...'
        self.setup_closure_compiler()
