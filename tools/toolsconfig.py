import ConfigParser
import re
import os


class ToolsConfig(object):
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
        path = self.parser.get('project', 'development')
        return os.path.normpath(path)

    def debug_dir(self):
        path = self.parser.get('project', 'debug')
        return os.path.normpath(path)

    def production_dir(self):
        path = self.parser.get('project', 'production')
        return os.path.normpath(path)

    def compiled_js(self):
        path = self.parser.get('project', 'compiled_js')
        return os.path.normpath(path)

    def test_file_pattern(self):
        return self.parser.get('project', 'test_file_pattern')

    def is_debug_enabled(self):
        return self.parser.getboolean('project', 'is_debug_enabled')

    def library_root(self):
        path = self.parser.get('library', 'root')
        return os.path.normpath(path)

    def compiler_root(self):
        path = self.parser.get('compiler', 'root')
        return os.path.normpath(path)

    def closurebuilder(self):
        dir = self.library_root()
        return os.path.join(dir, 'closure', 'bin', 'build', 'closurebuilder.py')

    def depswriter(self):
        dir = self.library_root()
        return os.path.join(dir, 'closure', 'bin', 'build', 'depswriter.py')

    def base_js(self):
        dir = self.library_root()
        return os.path.join(dir, 'closure', 'goog', 'base.js')

    def multitestrunner_css(self):
        dir = self.library_root()
        return os.path.join(dir, 'closure', 'goog', 'css', 'multitestrunner.css')

    def js_dev_dir(self):
        dir = self.development_dir()
        return os.path.join(dir, 'js_dev')

    def deps_js(self):
        dir = self.js_dev_dir()
        return os.path.join(dir, 'deps.js')

    def testrunner(self):
        dir = self.development_dir()
        return os.path.join(dir, 'all_tests.html')

    def compiler(self):
        dir = self.compiler_root()
        return os.path.join(dir, 'compiler.jar')

    def compilation_level(self):
        return self.parser.get('compiler', 'compilation_level')
