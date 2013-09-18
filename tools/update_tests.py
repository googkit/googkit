#!/usr/bin/env python


import os
import toolsconfig


CONFIG = os.path.join('tools', 'tools.cfg')


def line_indent(line):
    indent = ''
    m = re.search(r'^(\s*)', line)
    if len(m.groups()) >= 1:
        indent = m.group(1)

    return indent


def get_test_file_names(config):
    file_names = []
    dev_dir = config.development_dir()
    test_file_regexp = re.compile(config.test_file_pattern())
    
    for root, dirs, files in os.walk(dev_dir):
        for file in files:
            path = os.path.join(root, file)

            if re.search(test_file_regexp, path) is not None:
                file_names.append(file)

    return ','.join(file_names)


def update_tests(config):
    path = '/'.join([config.development_dir(), 'test_all.html'])
    marker = '/*@test_files@*/'
    lines = []

    for line in open(path):
        if line.find(marker) >= 0:
            line = line_indent(line) + 'var testFiles = [%s];%s\n' % (get_test_file_names(config), marker)

        lines.append(line)

    with open(path, 'w') as f:
        for line in lines:
            f.write(line)


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    config = toolsconfig.ToolsConfig()
    config.load(CONFIG)



    update_tests(config)
