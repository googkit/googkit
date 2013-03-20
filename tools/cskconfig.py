import ConfigParser
import os


class CskConfig(object):
    def __init__(self):
        pass

    def load(self, path):
        parser = ConfigParser.ConfigParser()

        with open(path) as f:
            parser.readfp(f)

        self.parser = parser

    def main_namespace(self):
        return self.parser.get('project', 'main_namespace')

    def development_dir(self):
        return self.parser.get('project', 'development')

    def production_dir(self):
        return self.parser.get('project', 'production')

    def compiled_js(self):
        return self.parser.get('project', 'compiled_js')

    def library_local_root(self):
        return self.parser.get('library', 'local_root')

    def library_global_root(self):
        return self.parser.get('library', 'global_root')

    def compiler_root(self):
        return self.parser.get('compiler', 'root')

    def closurebuilder(self):
        dir = self.library_local_root()
        return os.path.join(dir, 'closure', 'bin', 'build', 'closurebuilder.py')

    def depswriter(self):
        dir = self.library_local_root()
        return os.path.join(dir, 'closure', 'bin', 'build', 'depswriter.py')

    def local_base_js(self):
        dir = self.library_local_root()
        return os.path.join(dir, 'closure', 'goog', 'base.js')

    def compiler(self):
        dir = self.compiler_root()
        return os.path.join(dir, 'compiler.jar')

    def compilation_level(self):
        return self.parser.get('compiler', 'compilation_level')
