import os
import subprocess
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


class FastSetupCommand(Command):
    def __init__(self, env):
        super(FastSetupCommand, self).__init__(env)


    @classmethod
    def needs_config(cls):
        return True


    @classmethod
    def needs_global_config(cls):
        return True


    @classmethod
    def symlink(cls, src, dst):
        src_path = os.path.abspath(src)
        dst_path = os.path.abspath(dst)

        if not os.path.exists(src_path):
            raise GoogkitError('Link target is not found: ' + src_path)
        if not os.path.isdir(src_path):
            raise GoogkitError('Link target is not directory: ' + src_path)

        if os.path.exists(dst_path):
            try:
                os.unlink(dst_path)
            except OSError:
                os.rmdir(dst_path)

        dst_dir = os.path.abspath(os.path.join(dst_path, '..'))

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        if hasattr(os, 'symlink'):
            os.symlink(src_path, dst_path)
        else:
            # Make a NTFS junction if run on Windows
            subprocess.check_call(['mklink', '/J', dst_path, src_path], shell = True)


    def link_closure_library(self):
        local_library_root = self.env.config.library_root()

        try:
            global_library_root = self.env.global_config.library_root()
        except NoOptionError:
            raise GoogkitError('No Closure Library Root in global config.')

        FastSetupCommand.symlink(global_library_root, local_library_root)


    def link_closure_compiler(self):
        local_compiler_root = self.env.config.compiler_root()

        try:
            global_compiler_root = self.env.global_config.compiler_root()
        except NoOptionError:
            raise GoogkitError('No Closure Compiler Root in global config.')

        FastSetupCommand.symlink(global_compiler_root, local_compiler_root)


    def run_internal(self):
        if (True):
            print('Linking Closure Library...')
            self.link_closure_library()

            print('Linking Closure Compiler...')
            self.link_closure_compiler()
