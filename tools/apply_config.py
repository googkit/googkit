#!/usr/bin/env python


import glob
import os
import re
import toolsconfig


CONFIG = os.path.join('tools', 'tools.cfg')


def line_indent(line):
    indent = ''
    m = re.search(r'^(\s*)', line)
    if len(m.groups()) >= 1:
        indent = m.group(1)

    return indent


def update_base_js(line, config):
    path = '/'.join([config.library_global_root(), 'closure', 'goog', 'base.js'])
    return '<script type="text/javascript" src="%s"></script>' % path


def update_require_main(line, config):
    namespace = config.main_namespace()
    return '<script type="text/javascript"> goog.require(\'%s\'); </script>' % namespace


def update_exec_main(line, config):
    namespace = config.main_namespace()
    return '%s();' % namespace


def update_provide_main(line, config):
    namespace = config.main_namespace()
    return 'goog.provide(\'%s\');' % namespace


def update_main_fn(line, config):
    namespace = config.main_namespace()
    return '%s = function() {' % namespace


def update_test_runner_css(line, config):
    path = '/'.join([config.library_global_root(), 'closure', 'goog', 'css', 'multitestrunner.css'])
    return '<link rel="stylesheet" type="text/css" href="%s">' % path


def apply_config(path, config):
    lines = []
    updaters = {
            '<!--@base_js@-->': update_base_js,
            '/*@exec_main@*/': update_exec_main,
            '/*@main_fn@*/': update_main_fn,
            '/*@provide_main@*/': update_provide_main,
            '<!--@require_main@-->': update_require_main,
            '<!--@test_runner_css@-->'}: update_test_runner_css
    markers = updaters.keys()

    for line in open(path):
        for marker in markers:
            if line.find(marker) >= 0:
                updater = updaters[marker]
                line = line_indent(line) + updater(line, config) + marker + '\n'
        lines.append(line)

    with open(path, 'w') as f:
        for line in lines:
            f.write(line)


def apply_config_all(config):
    dev_dir = config.development_dir()
    for root, dirs, files in os.walk(dev_dir):
        for file in files:
            path = os.path.join(root, file)
            apply_config(path, config)


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    config = toolsconfig.ToolsConfig()
    config.load(CONFIG)

    apply_config_all(config)
