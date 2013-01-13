#!/usr/bin/env python


import re
import sys


def compile_index_html(path, compiled_js_path):
    lines = []

    for line in open(path):
        # Remove lines that requires unneeded scripts
        if re.search(r'closure/goog/base\.js', line) is not None:
            continue
        if re.search(r'goog\.require', line) is not None:
            continue

        # Replace deps.js by a compiled script
        line = re.sub(r'js_dev/deps\.js', compiled_js_path, line)
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
