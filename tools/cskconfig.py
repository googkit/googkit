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

    def library_dir(self):
        return self.parser.get('path', 'library')

    def compiler_dir(self):
        return self.parser.get('path', 'compiler')

    def closurebuilder(self):
        dir = self.library_dir()
        return os.path.join(dir, 'closure', 'bin', 'build', 'closurebuilder.py')

    def depswriter(self):
        dir = self.library_dir()
        return os.path.join(dir, 'closure', 'bin', 'build', 'depswriter.py')

    def compiler(self):
        dir = self.compiler_dir()
        return os.path.join(dir, 'compiler.jar')

    def development_dir(self):
        return self.parser.get('path', 'development')

    def production_dir(self):
        return self.parser.get('path', 'production')
