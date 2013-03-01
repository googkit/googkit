#!/usr/bin/env python


CONFIG = 'config.cfg'


import os
import cskconfig


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    config = cskconfig.CskConfig()
    config.load(CONFIG)

    devel_dir = config.development_dir()
    os.system('python %s --root_with_prefix="%s/js_dev ../../../../%s/js_dev" --output_file="%s/js_dev/deps.js"' % (config.depswriter(), devel_dir, devel_dir, devel_dir))
