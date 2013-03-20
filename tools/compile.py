#!/usr/bin/env python


import os
import shutil
import cskconfig


CONFIG = os.path.join('tools', 'config.cfg')


def rmtree_silent(path):
    try:
        shutil.rmtree(path)
    except OSError:
        pass


def setup_production_files(config):
    devel_dir = config.development_dir()
    prod_dir = config.production_dir()

    rmtree_silent(prod_dir)

    shutil.copytree(devel_dir, prod_dir)

    subtool_compile_index = os.path.join('tools', 'sub', 'compile_index.py')
    prod_index_html = os.path.join(prod_dir, 'index.html')
    compiled_js = config.compiled_js()
    os.system('python %s %s %s' % (subtool_compile_index, prod_index_html, compiled_js))


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

    config = cskconfig.CskConfig()
    config.load(CONFIG)

    setup_production_files(config)
    compile_scripts(config)
