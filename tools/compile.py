#!/usr/bin/env python


import os
import re
import shutil
import toolsconfig
import json


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
        if line.find('<!--@deps_js@-->') >= 0:
            continue

        # Replace deps.js by a compiled script
        if line.find('<!--@require_main@-->') >= 0:
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
    devel_dir = config.development_dir()
    prod_dir = config.production_dir()
    js_dev_dir = os.path.join(devel_dir, 'js_dev')
    compiled_js = config.compiled_js()
    prod_compiled_js = os.path.join(prod_dir, compiled_js)

    source_map = compiled_js + '.map'
    prod_source_map = os.path.join(prod_dir, source_map)
    rmtree_silent(os.path.join(prod_dir, 'js_dev'))

    args = [
            '--root=' + config.library_local_root(),
            '--root=' + js_dev_dir,
            '--namespace=' + config.main_namespace(),
            '--output_mode=compiled',
            '--compiler_jar=' + config.compiler(),
            '--compiler_flags=--compilation_level=' + config.compilation_level(),
            '--compiler_flags=--source_map_format=V3',
            '--compiler_flags=--create_source_map=' + prod_source_map,
            '--compiler_flags=--output_wrapper="%output%//# sourceMappingURL=' + source_map + '"',
            '--output_file=' + prod_compiled_js]
    os.system('python %s %s' % (config.closurebuilder(), ' '.join(args)))

    # In default, the source map file marks original sources to the same directory as "production".
    # But the original sources are in "closure" or "development/js_dev", so we should set a source
    # map attribute as "sourceRoot" to fix the original source paths.
    # But cannot set the "sourceRoot" by Closure Compiler yet, so "modify_source_map" does it
    # until Closure Compiler support "sourceRoot".
    modify_source_map(config)


def modify_source_map(config):
    prod_dir = config.production_dir()
    source_map = config.compiled_js() + '.map'
    prod_source_map = os.path.join(prod_dir, source_map)

    with open(prod_source_map, 'r+') as source_map_file:
        source_map_content = json.load(source_map_file)
        source_map_content['sourceRoot'] = '../'

        source_map_file.seek(0)
        json.dump(source_map_content, source_map_file)
        source_map_file.truncate()


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    config = toolsconfig.ToolsConfig()
    config.load(CONFIG)

    setup_production_files(config)
    compile_scripts(config)
