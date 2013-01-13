#!/usr/bin/env python


import os


DEPS_WRITER = 'closure/library/closure/bin/build/depswriter.py'


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    os.system('python %s --root_with_prefix="debug/js_dev ../../../../debug/js_dev" --output_file="debug/js_dev/deps.js"' % DEPS_WRITER)
