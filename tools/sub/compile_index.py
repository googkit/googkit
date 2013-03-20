#!/usr/bin/env python


import re
import sys


def line_indent(line):
    indent = ''
    m = re.search(r'^(\s*)', line)
    if len(m.groups()) >= 1:
        indent = m.group(1)

    return indent


def compile_index_html(path, compiled_js_path):
    lines = []

    for line in open(path):
        # Remove lines that requires unneeded scripts
        if line.find('<!--@base_js@-->') >= 0:
            continue
        if line.find('/*@require_main@*/') >= 0:
            continue

        # Replace deps.js by a compiled script
        if line.find('<!--@deps_js@-->') >= 0:
            indent = line_indent(line)
            line = '%s<script type="text/javascript" src="%s"></script>\n' % (indent, compiled_js_path)

        lines.append(line)

    with open(path, 'w') as f:
        for line in lines:
            f.write(line)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s input_path compiled_js_path' % sys.argv[0]
        sys.exit()

    path = sys.argv[1]
    compiled_js_path = sys.argv[2]
    compile_index_html(path, compiled_js_path)
