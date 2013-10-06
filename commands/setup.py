import os
import os.path
import subprocess
import ctypes
import shutil
import lib.clone
import lib.download
import lib.unzip
from command import Command
from lib.error import GoogkitError

NoOptionError = None
try:
    # Python 2.x
    import ConfigParser
    NoOptionError = ConfigParser.NoOptionError
except ImportError:
    # Python 3.x or later
    import configparser
    NoOptionError = configparser.NoOptionError


class SetupCommand(Command):
    LIBRARY_GIT_REPOS = 'https://code.google.com/p/closure-library/'
    COMPILER_LATEST_ZIP = 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'


    def __init__(self, env):
        super(SetupCommand, self).__init__(env)


    @classmethod
    def needs_config(cls):
        return True


    @classmethod
    def needs_global_config(cls):
        return True


    @classmethod
    def safe_mkdirs(cls, path):
        shutil.rmtree(path, True)
        os.makedirs(path)


    @classmethod
    def link(cls, src, dst):
        src_path = os.path.abspath(src)
        dst_path = os.path.abspath(dst)

        if not os.path.exists(src_path):
            raise GoogkitError('Link target is not found: ' + src_path)
        if not os.path.isdir(src_path):
            raise GoogkitError('Link target is not directory: ' + src_path)

        if os.path.exists(dst_path):
            try:
                os.unlink(dst_path)
            except WindowsError:
                os.rmdir(dst_path)

        dst_dir = os.path.abspath(os.path.join(dst_path, '..'))

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        if hasattr(os, 'link'):
            os.link(src_path, dst_path)
        else:
            # Make a NTFS junction if run on Windows
            subprocess.check_call(['mklink', '/J', dst_path, src_path], shell = True)


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


    def link_closure_library(self):
        local_library_root = self.env.config.library_root()

        try:
            global_library_root = self.env.global_config.library_root()
        except NoOptionError:
            raise GoogkitError('No Closure Library Root in global config.')

        SetupCommand.link(global_library_root, local_library_root)


    def link_closure_compiler(self):
        local_compiler_root = self.env.config.compiler_root()

        try:
            global_compiler_root = self.env.global_config.compiler_root()
        except NoOptionError:
            raise GoogkitError('No Closure Compiler Root in global config.')

        SetupCommand.link(global_compiler_root, local_compiler_root)


    def run_internal(self):
        # TODO: Implement arguments
        if (True):
            print('Linking Closure Library...')
            self.link_closure_library()

            print('Linking Closure Compiler...')
            self.link_closure_compiler()
        else:
            print('Downloading Closure Library...')
            #self.setup_closure_library()

            print('Downloading Closure Compiler...')
            #self.setup_closure_compiler()
