#!/usr/bin/env python


CLOSURE_BUILDER = 'closure/library/closure/bin/build/closurebuilder.py'
COMPILER_FLAGS = '--compilation_level=ADVANCED_OPTIMIZATIONS'
COMPILED_JS = 'script.min.js'
NAMESPACE_MAIN = 'com.mycompany.Main'


import os
import shutil


def rmtree_silent(path):
    try:
        shutil.rmtree(path)
    except OSError:
        pass


def setup_release_files():
    rmtree_silent('release')

    shutil.copytree('debug', 'release')
    os.system('python tools/sub/compile_index.py release/index.html ' + COMPILED_JS)


def compile_scripts():
    os.remove('release/js_dev/deps.js')

    args = [
            '--root=closure/library',
            '--root=release/js_dev',
            '-n ' + NAMESPACE_MAIN,
            '-o compiled',
            '-c closure/compiler/compiler.jar',
            '--compiler_flags=' + COMPILER_FLAGS,
            '--output_file=release/' + COMPILED_JS]
    os.system('python %s %s' % (CLOSURE_BUILDER, ' '.join(args)))
    rmtree_silent('release/js_dev')


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    setup_release_files()
    compile_scripts()
