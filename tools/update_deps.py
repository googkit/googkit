#!/usr/bin/env python


CONFIG = 'config.cfg'


import os
import cskconfig


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    config = cskconfig.CskConfig()
    config.load(CONFIG)

    os.system('python %s --root_with_prefix="debug/js_dev ../../../../debug/js_dev" --output_file="debug/js_dev/deps.js"' % config.depswriter())
