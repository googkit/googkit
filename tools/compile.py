#!/usr/bin/env python


import os
import re
import shutil
import toolsconfig


CONFIG = os.path.join('tools', 'tools.cfg')
COMPILE_TARGET_PATTERN = r'\.(html|xhtml)$'


def rmtree_silent(path):
    try:
        shutil.rmtree(path)
    except OSError:
        pass


def line_indent(line):
    indent = ''
    m = re.search(r'^(\s*)', line)
    if len(m.groups()) >= 1:
        indent = m.group(1)

    return indent


def compile_resource(path, compiled_js_path):
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


def setup_production_files(config):
    devel_dir = config.development_dir()
    prod_dir = config.production_dir()
    compiled_js = config.compiled_js()

    rmtree_silent(prod_dir)
    shutil.copytree(devel_dir, prod_dir)

    for root, dirs, files in os.walk(prod_dir):
        for file in files:
            path = os.path.join(root, file)
            if re.search(COMPILE_TARGET_PATTERN, path) is None:
                continue

            compile_resource(path, compiled_js)


def compile_scripts(config):
    prod_dir = config.production_dir()
    js_dev_dir = os.path.join(prod_dir, 'js_dev')
    compiled_js = config.compiled_js()
    prod_compiled_js = os.path.join(prod_dir, compiled_js)

    os.remove(os.path.join(js_dev_dir, 'deps.js'))

    args = [
            '--root=' + config.library_local_root(),
            '--root=' + js_dev_dir,
            '-n ' + config.main_namespace(),
            '-o compiled',
            '-c ' + config.compiler(),
            '--compiler_flags=--compilation_level=' + config.compilation_level(),
            '--output_file=' + prod_compiled_js]
    os.system('python %s %s' % (config.closurebuilder(), ' '.join(args)))
    rmtree_silent(js_dev_dir)


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    config = toolsconfig.ToolsConfig()
    config.load(CONFIG)

    setup_production_files(config)
    compile_scripts(config)
