import logging
import os
import shutil
import tempfile
import googkit.lib.clone
import googkit.lib.download
import googkit.lib.unzip
from googkit.cmds.command import Command
from googkit.lib.error import GoogkitError


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
            googkit.lib.clone.run(SetupCommand.LIBRARY_GIT_REPOS, self.env.config.library_root())
        except GoogkitError as e:
            raise GoogkitError('Dowloading Closure Library failed: ' + str(e))

    def setup_closure_compiler(self):
        tmp_path = tempfile.mkdtemp()
        compiler_zip = os.path.join(tmp_path, 'compiler.zip')

        try:
            googkit.lib.download.run(SetupCommand.COMPILER_LATEST_ZIP, compiler_zip)
        except IOError as e:
            raise GoogkitError('Dowloading Closure Compiler failed: ' + str(e))

        compiler_root = self.env.config.compiler_root()

        os.path.join('tools', 'sub', 'unzip.py')
        googkit.lib.unzip.run(compiler_zip, compiler_root)

        shutil.rmtree(tmp_path)

    def run_internal(self):
        logger = logging.getLogger()
        level = logger.level
        if self.env.arg_parser.option('--verbose'):
            logger.setLevel(logging.DEBUG)

        logging.info('Downloading Closure Library...')
        self.setup_closure_library()

        logging.info('Downloading Closure Compiler...')
        self.setup_closure_compiler()

        logger.setLevel(level)
