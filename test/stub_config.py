import os.path


# This stub simulates:
#
# dir1
# |-- dir2
# |   |-- DEVELOPMENT
# |   |   |-- ALL_TESTS.HTML
# |   |   +-- JS_DEV
# |   |       +-- DEPS.JS
# |   |
# |   |-- DEBUG
# |   |   |-- SCRIPT.MIN.JS
# |   |   +-- SCRIPT.MIN.JS.map
# |   |
# |   +-- PRODUCTION
# |       |-- SCRIPT.MIN.JS
# |       +-- SCRIPT.MIN.JS.map
# |
# +-- CLOSURE
#     |-- COMPILER
#     +-- LIBRARY
#         +-- CLOSURE
#             |-- GOOG
#             |   +-- BASE.JS
#             |
#             +-- CSS
#                 +-- MULTITESTRUNNER.CSS
#
class StubConfig(object):
    def __init__(self):
        pass

    def development_dir(self):
        return StubConfig.DEVELOPMENT_DIR

    def debug_dir(self):
        return StubConfig.DEBUG_DIR

    def production_dir(self):
        return StubConfig.PRODUCTION_DIR

    def compiled_js(self):
        return StubConfig.COMPILED_JS

    def test_file_pattern(self):
        return StubConfig.TEST_FILE_PATTERN

    def is_debug_enabled(self):
        return True

    def library_root(self):
        return StubConfig.LIBRARRY_ROOT

    def closurebuilder(self):
        return StubConfig.CLOSUREBUILDER

    def depswriter(self):
        return StubConfig.DEPSWRITER

    def compiler_root(self):
        return StubConfig.COMPILER_ROOT

    def base_js(self):
        return StubConfig.BASE_JS

    def multitestrunner_css(self):
        return StubConfig.MULTI_TEST_RUNNER_CSS

    def js_dev_dir(self):
        return StubConfig.JS_DEV_DIR

    def deps_js(self):
        return StubConfig.DEPS_JS

    def testrunner(self):
        return StubConfig.TESTRUNNER

    def compiler(self):
        return StubConfig.COMPILER

    def compilation_level(seld):
        return StubConfig.COMPILATION_LEVEL


StubConfig.PROJECT_DIR = os.path.join(os.sep, 'dir1')

StubConfig.LIBRARRY_ROOT = os.path.join(
    StubConfig.PROJECT_DIR, 'CLOSURE', 'LIBRARY')

StubConfig.COMPILER_ROOT = os.path.join(
    StubConfig.PROJECT_DIR, 'CLOSURE', 'COMPILER')

StubConfig.DEVELOPMENT_DIR = os.path.join(
    StubConfig.PROJECT_DIR, 'dir2', 'DEVELOPMENT')

StubConfig.DEBUG_DIR = os.path.join(
    StubConfig.PROJECT_DIR, 'dir2', 'DEBUG')

StubConfig.PRODUCTION_DIR = os.path.join(
    StubConfig.PROJECT_DIR, 'dir2', 'PRODUCTION')

StubConfig.JS_DEV_DIR = os.path.join(
    StubConfig.DEVELOPMENT_DIR, 'JS_DEV')

StubConfig.TESTRUNNER = os.path.join(
    StubConfig.DEVELOPMENT_DIR, 'ALL_TESTS.HTML')

StubConfig.DEPS_JS = os.path.join(
    StubConfig.JS_DEV_DIR, 'DEPS.JS')

StubConfig.BASE_JS = os.path.join(
    StubConfig.LIBRARRY_ROOT, 'CLOSURE', 'GOOG', 'BASE.JS')

StubConfig.MULTI_TEST_RUNNER_CSS = os.path.join(
    StubConfig.LIBRARRY_ROOT, 'CLOSURE', 'CSS', 'MULTITESTRUNNER.CSS')

StubConfig.CLOSUREBUILDER = os.path.join(
    StubConfig.LIBRARRY_ROOT, 'CLOSURE', 'BIN', 'BUILD', 'CLOSUREBUILDER.PY')

StubConfig.DEPSWRITER = os.path.join(
    StubConfig.LIBRARRY_ROOT, 'CLOSURE', 'BIN', 'BUILD', 'DEPSWRITER.PY')

StubConfig.COMPILER = os.path.join(
    StubConfig.COMPILER_ROOT, 'compiler.jar')

StubConfig.TEST_FILE_PATTERN = '_TEST\.(HTML|XHTML)$'
StubConfig.COMPILED_JS = 'SCRIPT.MIN.JS'
StubConfig.COMPILATION_LEVEL = 'COMPILATION_LEVEL'


# This stub is useful when test target includes "os.walk()".
# os.walk is hard to make the mock, so instead to use stub and
# walking into "googkit/test/stub_project".
#
# This stub simulates:
#
# googkit
# +-- test
#     +-- fixture
#         +-- stub_project
#             |
#             |-- development
#             |   |-- all_tests.html
#             |   +-- js_dev
#             |       +-- deps.js
#             |
#             |-- debug
#             |   |-- script.min.js
#             |   +-- script.min.js.map
#             |
#             |-- production
#             |   |-- script.min.js
#             |   +-- script.min.js.map
#             |
#             +-- closure
#                 |-- compiler
#                 +-- library
#                     +-- closure
#                         |-- goog
#                         |   +-- base.js
#                         |
#                         +-- css
#                             +-- multitestrunner.css
#
class StubConfigOnStubProject(object):
    def __init__(self):
        pass

    def development_dir(self):
        return StubConfigOnStubProject.DEVELOPMENT_DIR

    def debug_dir(self):
        return StubConfigOnStubProject.DEBUG_DIR

    def production_dir(self):
        return StubConfigOnStubProject.PRODUCTION_DIR

    def compiled_js(self):
        return StubConfigOnStubProject.COMPILED_JS

    def test_file_pattern(self):
        return StubConfigOnStubProject.TEST_FILE_PATTERN

    def is_debug_enabled(self):
        return True

    def library_root(self):
        return StubConfigOnStubProject.LIBRARRY_ROOT

    def closurebuilder(self):
        return StubConfigOnStubProject.CLOSUREBUILDER

    def depswriter(self):
        return StubConfigOnStubProject.DEPSWRITER

    def compiler_root(self):
        return StubConfigOnStubProject.COMPILER_ROOT

    def base_js(self):
        return StubConfigOnStubProject.BASE_JS

    def multitestrunner_css(self):
        return StubConfigOnStubProject.MULTI_TEST_RUNNER_CSS

    def js_dev_dir(self):
        return StubConfigOnStubProject.JS_DEV_DIR

    def deps_js(self):
        return StubConfigOnStubProject.DEPS_JS

    def testrunner(self):
        return StubConfigOnStubProject.TESTRUNNER

    def compiler(self):
        return StubConfigOnStubProject.COMPILER

    def compilation_level(self):
        return StubConfigOnStubProject.COMPILATION_LEVEL


StubConfigOnStubProject.PROJECT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixture', 'stub_project'))

StubConfigOnStubProject.LIBRARRY_ROOT = os.path.join(
    StubConfigOnStubProject.PROJECT_DIR, 'CLOSURE', 'LIBRARY')

StubConfigOnStubProject.COMPILER_ROOT = os.path.join(
    StubConfigOnStubProject.PROJECT_DIR, 'CLOSURE', 'COMPILER')

StubConfigOnStubProject.DEVELOPMENT_DIR = os.path.join(
    StubConfigOnStubProject.PROJECT_DIR, 'development')

StubConfigOnStubProject.DEBUG_DIR = os.path.join(
    StubConfigOnStubProject.PROJECT_DIR, 'debug')

StubConfigOnStubProject.PRODUCTION_DIR = os.path.join(
    StubConfigOnStubProject.PROJECT_DIR, 'production')

StubConfigOnStubProject.JS_DEV_DIR = os.path.join(
    StubConfigOnStubProject.DEVELOPMENT_DIR, 'js_dev')

StubConfigOnStubProject.TESTRUNNER = os.path.join(
    StubConfigOnStubProject.DEVELOPMENT_DIR, 'all_tests.html')

StubConfigOnStubProject.DEPS_JS = os.path.join(
    StubConfigOnStubProject.JS_DEV_DIR, 'deps.js')

StubConfigOnStubProject.BASE_JS = os.path.join(
    StubConfigOnStubProject.LIBRARRY_ROOT, 'CLOSURE', 'GOOG', 'BASE.JS')

StubConfigOnStubProject.MULTI_TEST_RUNNER_CSS = os.path.join(
    StubConfigOnStubProject.LIBRARRY_ROOT, 'CLOSURE', 'CSS', 'MULTITESTRUNNER.CSS')

StubConfigOnStubProject.CLOSUREBUILDER = os.path.join(
    StubConfigOnStubProject.LIBRARRY_ROOT, 'CLOSURE', 'BIN', 'BUILD', 'CLOSUREBUILDER.PY')

StubConfigOnStubProject.DEPSWRITER = os.path.join(
    StubConfigOnStubProject.LIBRARRY_ROOT, 'CLOSURE', 'BIN', 'BUILD', 'DEPSWRITER.PY')

StubConfigOnStubProject.COMPILER = os.path.join(
    StubConfigOnStubProject.COMPILER_ROOT, 'compiler.jar')

StubConfigOnStubProject.COMPILED_JS = 'script.min.js'
StubConfigOnStubProject.TEST_FILE_PATTERN = '_test\.(html|xhtml)$'
StubConfigOnStubProject.COMPILATION_LEVEL = '%COMPILATION_LEVEL%'
