import os.path

# Expected following directory structure:
#
# dir1
# |-- dir2 
# |   +-- DEVELOPMENT
# |       +-- JS_DEV
# |           +-- DEPS.JS
# +-- CLOSURE
#     |-- COMPILER
#     +-- LIBRARY
#         +-- CLOSURE
#             |-- GOOG
#             |   +-- BASE.JS
#             +-- CSS
#                 +-- MULTITESTRUNNER.CSS
#
PROJECT_DIR = os.path.join(os.sep, 'dir1')

LIBRARRY_ROOT = os.path.join(PROJECT_DIR, 'CLOSURE', 'LIBRARY')
COMPILER_ROOT = os.path.join(PROJECT_DIR, 'CLOSURE', 'COMPILER')

DEVELOPMENT_DIR = os.path.join(PROJECT_DIR, 'dir2', 'DEVELOPMENT')
DEBUG_DIR = os.path.join(PROJECT_DIR, 'dir2', 'DEBUG')
PRODUCTION_DIR = os.path.join(PROJECT_DIR, 'dir2', 'PRODUCTION')

JS_DEV_DIR = os.path.join(DEVELOPMENT_DIR, 'JS_DEV')
TESTRUNNER = os.path.join(DEVELOPMENT_DIR, 'ALL_TESTS.HTML')

DEPS_JS = os.path.join(JS_DEV_DIR, 'DEPS.JS')

BASE_JS = os.path.join(LIBRARRY_ROOT, 'CLOSURE', 'GOOG', 'BASE.JS')
CLOSUREBUILDER = os.path.join(LIBRARRY_ROOT, 'CLOSURE', 'BIN', 'BUILD', 'CLOSUREBUILDER.PY')
MULTI_TEST_RUNNER_CSS = os.path.join(LIBRARRY_ROOT, 'CLOSURE', 'CSS', 'MULTITESTRUNNER.CSS')

TEST_FILE_PATTERN = '_TEST\.(HTML|XHTML)$'
COMPILED_JS = '%COMPILED_JS%'
COMPILATION_LEVEL = '%COMPILATION_LEVEL%'


class StubConfig(object):
    def __init__(self):
        pass

    def development_dir(self):
        return DEVELOPMENT_DIR

    def debug_dir(self):
        return DEBUG_DIR

    def production_dir(self):
        return PRODUCTION_DIR

    def compiled_js(self):
        return COMPILED_JS

    def test_file_pattern(self):
        return TEST_FILE_PATTERN

    def is_debug_enabled(self):
        return True

    def library_root(self):
        return LIBRARRY_ROOT

    def closurebuilder(self):
        return CLOSUREBUILDER

    def compiler_root(self):
        return COMPILER_ROOT

    def base_js(self):
        return BASE_JS

    def multitestrunner_css(self):
        return MULTI_TEST_RUNNER_CSS

    def js_dev_dir(self):
        return JS_DEV_DIR

    def deps_js(self):
        return DEPS_JS

    def testrunner(self):
        return TESTRUNNER

    def compiler(self):
        return COMPILER

    def compilation_level(seld):
        return COMPILATION_LEVEL


STUB_PROJECT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixture', 'stub_project'))
DEVELOPMENT_DIR_IN_STUB_PROJECT = os.path.join(STUB_PROJECT, 'development')
DEBUG_DIR_IN_STUB_PRODUCTION = os.path.join(STUB_PROJECT, 'debug')
PRODUTION_DIR_IN_STUB_PROJECT = os.path.join(STUB_PROJECT, 'production')

JS_DEV_DIR_IN_STUB_PROJECT = os.path.join(DEVELOPMENT_DIR_IN_STUB_PROJECT, 'js_dev')
TESTRUNNER_IN_STUB_PROJECT = os.path.join(DEVELOPMENT_DIR_IN_STUB_PROJECT, 'all_tests.html')

DEPS_JS_IN_STUB_PROJECT = os.path.join(JS_DEV_DIR_IN_STUB_PROJECT, 'deps.js')


class StubConfigOnStubProject(object):
    def __init__(self):
        pass

    def development_dir(self):
        return DEVELOPMENT_DIR_IN_STUB_PROJECT

    def debug_dir(self):
        return DEBUG_DIR_IN_STUB_PRODUCTION

    def production_dir(self):
        return PRODUCTION_DIR_IN_STUB_PROJECT

    def compiled_js(self):
        return COMPILED_JS

    def test_file_pattern(self):
        return TEST_FILE_PATTERN

    def is_debug_enabled(self):
        return True

    def library_root(self):
        return LIBRARRY_ROOT

    def closurebuilder(self):
        return CLOSUREBUILDER

    def compiler_root(self):
        return COMPILER_ROOT

    def base_js(self):
        return BASE_JS

    def multitestrunner_css(self):
        return MULTI_TEST_RUNNER_CSS

    def js_dev_dir(self):
        return JS_DEV_DIR_IN_STUB_PROJECT

    def deps_js(self):
        return DEPS_JS_IN_STUB_PROJECT

    def testrunner(self):
        return TESTRUNNER_IN_STUB_PROJECT

    def compiler(self):
        return COMPILER

    def compilation_level(self):
        return COMPILATION_LEVEL
