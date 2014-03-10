import os
import googkit.compat.configparser as configparser


class Config(object):
    def __init__(self):
        self.parser = configparser.ConfigParser()

    def __load_if_necessary(self, path):
        if path is None:
            return

        with open(path) as fp:
            if hasattr(self.parser, 'read_file'):
                # Python 3.2 or later
                self.parser.read_file(fp)
            else:
                # Python 3.1 or earlier
                self.parser.readfp(fp)

    def load(self, project_path, user_path, default_path):
        """Loads 3 config files (project config, user config, default config).

        Config priority is:
        1. In project config file (PROJECT_DIR/googkit.cfg)
        2. In user config file (~/.googkit)
        3. In default config file (default.cfg)
        """
        self.__load_if_necessary(default_path)
        self.__load_if_necessary(user_path)
        self.__load_if_necessary(project_path)

    def development_dir(self):
        """Returns a directory path for the development resources.
        This config is a "development" option is in the "project" section.
        """
        path = self.parser.get('project', 'development')
        return os.path.normpath(path)

    def debug_dir(self):
        """Returns a directory path for the debugging resources.
        This config is a "debug" option is in the "project" section.
        """
        path = self.parser.get('project', 'debug')
        return os.path.normpath(path)

    def production_dir(self):
        """Returns a directory path for the production resources.
        This config is a "production" option is in the "project" section.
        """
        path = self.parser.get('project', 'production')
        return os.path.normpath(path)

    def compiled_js_ext(self):
        """Returns a file extension for the compiled script.
        This config is a "compiled_js_ext" option is in the "project" section.
        """
        return self.parser.get('project', 'compiled_js_ext')

    def no_built_js_pattern(self):
        """Returns a file name pattern of HTML requiring no JavaScript.
        This config is a "no_built_js_pattern" option is in the "project"
        section.
        """
        return self.parser.get('project', 'no_built_js_pattern')

    def test_file_pattern(self):
        """Returns a regular expression for the unit-test file pattern.
        This config is a "test_file_pattern" option is in the "project" section.
        """
        return self.parser.get('project', 'test_file_pattern')

    def library_root(self):
        """Returns a path for the Closure Library root directory.
        This config is a "root" option is in the "library" section.
        """
        path = self.parser.get('library', 'root')
        return os.path.normpath(path)

    def compiler_root(self):
        """Returns a path for the Closure Compiler root directory.
        This config is a "root" option is in the "compiler" section.
        """
        path = self.parser.get('compiler', 'root')
        return os.path.normpath(path)

    def closurebuilder(self):
        """Returns a path for the closurebuilder.py.
        """
        dir = self.library_root()
        return os.path.join(dir, 'closure', 'bin', 'build', 'closurebuilder.py')

    def depswriter(self):
        """Returns a path for the depswriter.py.
        """
        dir = self.library_root()
        return os.path.join(dir, 'closure', 'bin', 'build', 'depswriter.py')

    def base_js(self):
        """Returns a path for the base.js.
        """
        dir = self.library_root()
        return os.path.join(dir, 'closure', 'goog', 'base.js')

    def multitestrunner_css(self):
        """Returns a path for the multitestrunner.css.
        """
        dir = self.library_root()
        return os.path.join(dir, 'closure', 'goog', 'css', 'multitestrunner.css')

    def js_dev_dir(self):
        """Returns a directory path for javascript resources on development.
        """
        dir = self.development_dir()
        return os.path.join(dir, 'js_dev')

    def deps_js(self):
        """Returns a path for the deps.js.
        """
        dir = self.js_dev_dir()
        return os.path.join(dir, 'deps.js')

    def testrunner(self):
        """Returns a path for the unit-test runner.
        """
        dir = self.development_dir()
        return os.path.join(dir, 'all_tests.html')

    def compiler(self):
        """Returns a path for the compiler.jar (part of Closure Compiler).
        """
        dir = self.compiler_root()
        return os.path.join(dir, 'compiler.jar')

    def compilation_level(self):
        """Returns a compilation level for Closure Compiler.
        See: https://developers.google.com/closure/compiler/docs/compilation_levels
        """
        return self.parser.get('compiler', 'compilation_level')

    def library_repos(self):
        """Returns a repositry URL of Closure Library.
        """
        return self.parser.get('library', 'git_repository')

    def compiler_zip(self):
        """Returns an URL for the Closure Compiler zip.
        """
        return self.parser.get('compiler', 'zip_url')

    def compiler_flagfile(self):
        """Returns a file name of the flagfile for Closure Compiler.
        """
        return self.parser.get('compiler', 'flagfile')

    def compiler_flagfile_for_debug(self):
        """Returns a file name of the flagfile for Closure Compiler.
        See: http://google-gflags.googlecode.com/svn/trunk/doc/gflags.html
        """
        return self.parser.get('compiler', 'flagfile_debug')

    def linter_flagfile(self):
        """Returns a file name of the flagfile for Closure Linter.
        See: http://google-gflags.googlecode.com/svn/trunk/doc/gflags.html
        """
        return self.parser.get('linter', 'flagfile')
