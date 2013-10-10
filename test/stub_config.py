import os.path

# Expected following directory structure:
#
# dir1
# |-- dir2 
# |   +-- development
# |       +-- js_dev
# |           +-- deps.js
# +-- closure
#     |-- compiler
#     +-- library
#         +-- closure
#             |-- goog
#             |   +-- base.js
#             +-- css
#                 +-- multitestrunner.css
#
LIBRARRY_ROOT = '/dir1/closure/library/'
COMPILER_ROOT = '/dir1/closure/compiler/'
DEVELOPMENT_DIR = '/dir1/dir2/development'
DEPS_JS = os.path.join(DEVELOPMENT_DIR, 'js_dev/deps.js')
BASE_JS = os.path.join(LIBRARRY_ROOT, 'closure/goog/base.js')
MULTI_TEST_RUNNER_CSS = os.path.join(LIBRARRY_ROOT, 'closure/css/multitestrunner.css')


class StubConfig(object):
    def __init__(self):
        pass

    def library_root(self):
        return LIBRARRY_ROOT

    def compiler_root(self):
        return COMPILER_ROOT

    def development_dir(self):
        return DEVELOPMENT_DIR

    def deps_js(self):
        return DEPS_JS

    def base_js(self):
        return BASE_JS

    def multitestrunner_css(self):
        return MULTI_TEST_RUNNER_CSS
