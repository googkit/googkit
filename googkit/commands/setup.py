import logging
import os
import shutil
import tempfile
import googkit.lib.clone
import googkit.lib.download
import googkit.lib.unzip
from googkit.commands.command import Command
from googkit.lib.error import GoogkitError


class SetupCommand(Command):
    def __init__(self, env):
        super(SetupCommand, self).__init__(env)

    @classmethod
    def needs_config(cls):
        return True

    def setup_closure_library(self):
        library_repos = self.env.config.library_repos()
        library_root = self.env.config.library_root()
        try:
            googkit.lib.clone.run(library_repos, library_root)
        except GoogkitError as e:
            raise GoogkitError('Dowloading Closure Library failed: ' + str(e))

    def setup_closure_compiler(self):
        tmp_path = tempfile.mkdtemp()
        compiler_zip = os.path.join(tmp_path, 'compiler.zip')
        compiler_zip_url = self.env.config.compiler_zip()

        try:
            googkit.lib.download.run(compiler_zip_url, compiler_zip)
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
