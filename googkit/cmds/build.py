import os
import logging
import subprocess
import re
import shutil
import json
import googkit.lib.path
from googkit.cmds.command import Command
from googkit.lib.error import GoogkitError


class BuildCommand(Command):
    COMPILE_TARGET_EXT = ('.html', '.xhtml')


    def __init__(self, env):
        super(BuildCommand, self).__init__(env)


    @classmethod
    def needs_config(cls):
        return True


    @classmethod
    def rmtree_silent(cls, path):
        try:
            shutil.rmtree(path)
        except OSError:
            pass


    @classmethod
    def line_indent(cls, line):
        indent = ''
        m = re.search(r'^(\s*)', line)
        if len(m.groups()) >= 1:
            indent = m.group(1)

        return indent


    def compile_resource(self, path, compiled_js_path):
        lines = []

        with open(path) as f:
            for line in f:
                # Remove lines that requires unneeded scripts
                if line.find('<!--@base_js@-->') >= 0:
                    continue
                if line.find('<!--@deps_js@-->') >= 0:
                    continue

                # Replace deps.js by a compiled script
                if line.find('<!--@require_main@-->') >= 0:
                    indent = BuildCommand.line_indent(line)
                    line = indent + '<script type="text/javascript" src="{src}"></script>\n'.format(src=compiled_js_path)

                lines.append(line)

        with open(path, 'w') as f:
            for line in lines:
                f.write(line)


    @classmethod
    def ignore_dirs(cls, *ignore_dirs):
        def ignoref(dirpath, files):
            return [filename for filename in files if (os.path.join(dirpath, filename) in ignore_dirs)]
        return ignoref


    def setup_files(self, target_dir):
        config = self.env.config
        devel_dir = config.development_dir()
        compiled_js = config.compiled_js()

        # Avoid to copy unnecessary files for production
        ignores = (
            config.testrunner(),
            config.library_root(),
            config.compiler_root(),
            config.js_dev_dir())

        BuildCommand.rmtree_silent(target_dir)
        shutil.copytree(devel_dir, target_dir, ignore=BuildCommand.ignore_dirs(*ignores))

        for root, dirs, files in os.walk(target_dir):
            for file in files:
                path = os.path.join(root, file)
                (base, ext) = os.path.splitext(path)
                if ext not in BuildCommand.COMPILE_TARGET_EXT:
                    continue

                self.compile_resource(path, compiled_js)


    def compile_scripts(self):
        config = self.env.config
        js_dev_dir = config.js_dev_dir()
        compiled_js = config.compiled_js()

        # The library path should be a relative path from the project root.
        # Because "sources" in the source map becomes absolute if an absolute path was
        # specified by "--root".Then, the absolute path creates a problem on http scheme.
        lib_path = os.path.relpath(config.library_root(), googkit.lib.path.project_root())

        if config.is_debug_enabled():
            logging.info('Copying resources for debug...')
            self.setup_files(config.debug_dir())

            source_map = compiled_js + '.map'
            debug_dir = config.debug_dir()
            debug_source_map = os.path.join(debug_dir, source_map)
            debug_compiled_js = os.path.join(debug_dir, compiled_js)

            debug_args = [
                'python',
                config.closurebuilder(),
                '--root=' + lib_path,
                '--root=' + js_dev_dir,
                '--namespace=main',
                '--output_mode=compiled',
                '--compiler_jar=' + config.compiler(),
                '--compiler_flags=--compilation_level=' + config.compilation_level(),
                '--compiler_flags=--source_map_format=V3',
                '--compiler_flags=--create_source_map=' + debug_source_map,
                '--compiler_flags=--output_wrapper="%output%//# sourceMappingURL={path}"'.format(path=source_map),
                '--output_file=' + debug_compiled_js]

            logging.info('Building for debug...')
            builder_debug = subprocess.Popen(debug_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result_debug = builder_debug.communicate()

            if builder_debug.returncode != 0:
                raise GoogkitError('Compilation failed: ' + result_debug[1])
            else:
                logging.debug(result_debug[0])


            # In default, the source map file marks original sources to the same directory as "debug".
            # But the original sources are in "closure" or "development/js_dev", so we should set a source
            # map attribute as "sourceRoot" to fix the original source paths.
            # But cannot set the "sourceRoot" by Closure Compiler yet, so "modify_source_map" does it
            # until Closure Compiler support "sourceRoot".
            self.modify_source_map()

        logging.info('Copying resources for production...')
        self.setup_files(config.production_dir())

        prod_dir = config.production_dir()
        prod_compiled_js = os.path.join(prod_dir, compiled_js)
        prod_args = [
            'python',
            config.closurebuilder(),
            '--root=' + lib_path,
            '--root=' + js_dev_dir,
            '--namespace=main',
            '--output_mode=compiled',
            '--compiler_jar=' + config.compiler(),
            '--compiler_flags=--compilation_level=' + config.compilation_level(),
            '--compiler_flags=--define=goog.DEBUG=false',
            '--output_file=' + prod_compiled_js]

        logging.info('Building for production...')
        builder_proc = subprocess.Popen(prod_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = builder_proc.communicate()

        if builder_proc.returncode != 0:
            raise GoogkitError('Compilation failed: ' + result[1])
        else:
            logging.debug(result[0])


    def modify_source_map(self):
        debug_dir = self.env.config.debug_dir()
        source_map = self.env.config.compiled_js() + '.map'
        debug_source_map = os.path.join(debug_dir, source_map)

        with open(debug_source_map) as source_map_file:
            source_map_content = json.load(source_map_file)
            source_map_content['sourceRoot'] = '../'

        with open(debug_source_map, 'w') as source_map_file:
            json.dump(source_map_content, source_map_file)


    def run_internal(self):
        self.compile_scripts()
