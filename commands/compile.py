import os
import re
import shutil
import json
from lib.error import GoogkitError


class CompileCommand(object):
    COMPILE_TARGET_EXT = ('.html', '.xhtml')


    def __init__(self, config):
        self.config = config


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

        for line in open(path):
            # Remove lines that requires unneeded scripts
            if line.find('<!--@base_js@-->') >= 0:
                continue
            if line.find('<!--@deps_js@-->') >= 0:
                continue

            # Replace deps.js by a compiled script
            if line.find('<!--@require_main@-->') >= 0:
                indent = CompileCommand.line_indent(line)
                line = '%s<script type="text/javascript" src="%s"></script>\n' % (indent, compiled_js_path)

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
        config = self.config
        devel_dir = config.development_dir()
        compiled_js = config.compiled_js()

        # Avoid to copy unnecessary files for production
        ignores = (
                config.testrunner(),
                config.library_root(),
                config.compiler_root(),
                config.js_dev_dir())

        CompileCommand.rmtree_silent(target_dir)
        shutil.copytree(devel_dir, target_dir, ignore = CompileCommand.ignore_dirs(*ignores))

        for root, dirs, files in os.walk(target_dir):
            for file in files:
                path = os.path.join(root, file)
                (base, ext) = os.path.splitext(path)
                if ext not in CompileCommand.COMPILE_TARGET_EXT:
                    continue

                self.compile_resource(path, compiled_js)


    def compile_scripts(self):
        config = self.config
        devel_dir = config.development_dir()
        js_dev_dir = config.js_dev_dir()
        compiled_js = config.compiled_js()

        if config.is_debug_enabled():
            self.setup_files(config.debug_dir())

            source_map = compiled_js + '.map'
            debug_dir = config.debug_dir()
            debug_source_map = os.path.join(debug_dir, source_map)
            debug_compiled_js = os.path.join(debug_dir, compiled_js)
            debug_args = [
                    '--root=' + config.library_root(),
                    '--root=' + js_dev_dir,
                    '--namespace=main',
                    '--output_mode=compiled',
                    '--compiler_jar=' + config.compiler(),
                    '--compiler_flags=--compilation_level=' + config.compilation_level(),
                    '--compiler_flags=--source_map_format=V3',
                    '--compiler_flags=--create_source_map=' + debug_source_map,
                    '--compiler_flags=--output_wrapper="%output%//# sourceMappingURL=' + source_map + '"',
                    '--output_file=' + debug_compiled_js]
            os.system('python %s %s' % (config.closurebuilder(), ' '.join(debug_args)))

            # In default, the source map file marks original sources to the same directory as "debug".
            # But the original sources are in "closure" or "development/js_dev", so we should set a source
            # map attribute as "sourceRoot" to fix the original source paths.
            # But cannot set the "sourceRoot" by Closure Compiler yet, so "modify_source_map" does it
            # until Closure Compiler support "sourceRoot".
            self.modify_source_map()

        self.setup_files(config.production_dir())

        prod_dir = config.production_dir()
        prod_compiled_js = os.path.join(prod_dir, compiled_js)
        prod_args = [
                '--root=' + config.library_root(),
                '--root=' + js_dev_dir,
                '--namespace=main',
                '--output_mode=compiled',
                '--compiler_jar=' + config.compiler(),
                '--compiler_flags=--compilation_level=' + config.compilation_level(),
                '--compiler_flags=--define=goog.DEBUG=false',
                '--output_file=' + prod_compiled_js]
        os.system('python %s %s' % (config.closurebuilder(), ' '.join(prod_args)))


    def modify_source_map(self):
        debug_dir = self.config.debug_dir()
        source_map = self.config.compiled_js() + '.map'
        debug_source_map = os.path.join(debug_dir, source_map)

        with open(debug_source_map, 'r+') as source_map_file:
            source_map_content = json.load(source_map_file)
            source_map_content['sourceRoot'] = '../'

            source_map_file.seek(0)
            json.dump(source_map_content, source_map_file)
            source_map_file.truncate()


    def run(self):
        if self.config is None:
            raise GoogkitError('No config file found.')

        self.compile_scripts()
        print('Completed.')
