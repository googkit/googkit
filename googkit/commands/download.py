import logging
import os
import shutil
import tempfile
import zipfile
import googkit.lib.clone
import googkit.lib.path
from googkit.lib.dirutil import working_directory
from googkit.commands.command import Command
from googkit.lib.error import GoogkitError
from googkit.compat.urllib import request


class DownloadCommand(Command):
    @classmethod
    def needs_project_config(cls):
        return True

    def download_closure_library(self):
        library_repos = self.config.library_repos()
        library_root = self.config.library_root()

        logging.info('Downloading Closure Library...')

        try:
            googkit.lib.clone.run(library_repos, library_root)
        except GoogkitError as e:
            raise GoogkitError('Dowloading Closure Library failed: ' + str(e))

        logging.info('Done.')

    def download_closure_compiler(self):
        tmp_path = tempfile.mkdtemp()
        compiler_zip = os.path.join(tmp_path, 'compiler.zip')
        compiler_zip_url = self.config.compiler_zip()

        logging.info('Downloading Closure Compiler...')

        try:
            request.urlretrieve(compiler_zip_url, compiler_zip)
        except IOError as e:
            raise GoogkitError('Dowloading Closure Compiler failed: ' + str(e))

        compiler_root = self.config.compiler_root()

        os.path.join('tools', 'sub', 'unzip.py')

        with zipfile.ZipFile(compiler_zip) as z:
            z.extractall(compiler_root)

        shutil.rmtree(tmp_path)

        logging.info('Done.')

    def run_internal(self):
        project_root = googkit.lib.path.project_root(self.env.cwd)
        with working_directory(project_root):
            self.download_closure_library()
            self.download_closure_compiler()
