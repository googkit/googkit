#!/usr/bin/env python


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


def html_path(path):
    return '/'.join(path.split(os.path.sep))


def update_deps(config):
    js_dev_dir = config.js_dev_dir()
    deps_js = config.deps_js()

    base_js_dir = os.path.dirname(config.base_js())
    js_dev_dir_rel = os.path.relpath(js_dev_dir, base_js_dir)

    os.system('python %s --root_with_prefix="%s %s" --output_file="%s"' % (config.depswriter(), js_dev_dir, js_dev_dir_rel, deps_js))


def update_tests(line, tests, config):
    joined = ','.join([('\'%s\'' % test_file) for test_file in tests])
    return 'var testFiles = [%s];' % joined


def update_testrunner(config):
    js_dev_dir = config.js_dev_dir()
    testrunner = config.testrunner()
    testrunner_dir = os.path.dirname(testrunner)
    test_file_pattern = config.test_file_pattern()
    tests = []

    for dirpath, dirnames, filenames in os.walk(js_dev_dir):
        for filename in filenames:
            if re.search(test_file_pattern, filename) is None:
                continue

            path = os.path.join(dirpath, filename)
            relpath = os.path.relpath(path, testrunner_dir)

            tests.append(relpath)

    lines = []

    for line in open(testrunner):
        marker = '/*@test_files@*/'
        if line.find(marker) >= 0:
            line = line_indent(line) + update_tests(line, tests, config) + marker + '\n'

        lines.append(line)

    with open(testrunner, 'w') as f:
        for line in lines:
            f.write(line)


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    config = toolsconfig.ToolsConfig()
    config.load(CONFIG)

    update_deps(config)
    update_testrunner(config)
