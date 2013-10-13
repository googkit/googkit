import logging
import os
import shutil
import tempfile
import lib.clone
import lib.download
import lib.unzip
from cmds.command import Command
from lib.error import GoogkitError


class SetupCommand(Command):
    LIBRARY_GIT_REPOS = 'https://code.google.com/p/closure-library/'
    COMPILER_LATEST_ZIP = 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'


    def __init__(self, env):
        super(SetupCommand, self).__init__(env)


    @classmethod
    def needs_config(cls):
        return True


    def setup_closure_library(self):
        try:
            lib.clone.run(SetupCommand.LIBRARY_GIT_REPOS, self.env.config.library_root())
        except GoogkitError as e:
            raise Googkit('Dowloading Closure Library was failed: ' + str(e))


    def setup_closure_compiler(self):
        tmp_path = tempfile.mkdtemp()
        compiler_zip = os.path.join(tmp_path, 'compiler.zip')

        try:
            lib.download.run(SetupCommand.COMPILER_LATEST_ZIP, compiler_zip)
        except IOError as e:
            raise Googkit('Dowloading Closure Compiler was failed: ' + str(e))

        compiler_root = self.env.config.compiler_root()

        os.path.join('tools', 'sub', 'unzip.py')
        lib.unzip.run(compiler_zip, compiler_root)

        shutil.rmtree(tmp_path)


    def run_internal(self):
        logging.info('Downloading Closure Library...')
        self.setup_closure_library()

        logging.info('Downloading Closure Compiler...')
        self.setup_closure_compiler()
