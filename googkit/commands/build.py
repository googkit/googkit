import os
import logging
import subprocess
import re
import shutil
import json
import googkit.lib.path
from googkit.commands.command import Command
from googkit.lib.error import GoogkitError
from googkit.lib.dirutil import working_directory


class BuildCommand(Command):
    COMPILE_TARGET_EXT = ('.html', '.xhtml')

    class BuilderArguments(object):
        """Argument builder for the Closure Builder.

        Usage::
            >>> args = BuildCommand.BuilderArguments()
            >>> args.builder_arg('--arg1', 'ARG1')
            >>> args.builder_arg('--arg2', 'ARG2')
            >>> args.compiler_arg('--arg3', 'ARG3')
            >>> str(args)
            --arg1=ARG1 --arg2=ARG2 --compiler_flags="--arg3=ARG3"
        """

        class BuilderArgumentEntry(object):
            def __init__(self, key, value):
                self.key = key
                self.value = value

            def __str__(self):
                return self.key + '=' + self.value

            def __repr__(self):
                return '<Builder Argument \'' + str(self) + '\'>'

            def __eq__(self, other):
                return self.key == other.key and self.value == other.value

            def __hash__(self):
                return hash(str(self))

        class CompilerArgumentEntry(object):
            def __init__(self, key, value):
                self.key = key
                self.value = value

            def __str__(self):
                return '--compiler_flags={key}={value}'.format(
                    key=self.key, value=self.value)

            def __repr__(self):
                return '<Compiler Argument \'' + str(self) + '\'>'

            def __eq__(self, other):
                return self.key == other.key and self.value == other.value

            def __hash__(self):
                return hash(str(self))

        def __init__(self):
            self._args = set()

        def __eq__(self, other):
            return self._args == other._args

        def __str__(self):
            return ' '.join([str(entry) for entry in self._args])

        def __iter__(self):
            return iter(self._args)

        def builder_arg(self, key, value):
            entry = self.BuilderArgumentEntry(key, value)
            self._args.add(entry)

        def compiler_arg(self, key, value):
            entry = self.CompilerArgumentEntry(key, value)
            self._args.add(entry)

    @classmethod
    def needs_project_config(cls):
        return True

    @classmethod
    def supported_options(cls):
        opts = super(BuildCommand, cls).supported_options()
        opts.add('--debug')
        return opts

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

    @classmethod
    def ignore_dirs(cls, *ignore_dirs):
        def ignoref(dirpath, files):
            return [filename for filename in files
                    if (os.path.join(dirpath, filename) in ignore_dirs)]
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

        BuildCommand.rmtree_silent(target_dir)
        shutil.copytree(devel_dir, target_dir,
                        ignore=BuildCommand.ignore_dirs(*ignores))

        for root, dirs, files in os.walk(target_dir):
            for file in files:
                path = os.path.join(root, file)
                (base, ext) = os.path.splitext(path)
                if ext not in BuildCommand.COMPILE_TARGET_EXT:
                    continue

                self.compile_resource(path, compiled_js)

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
                    script = '<script src="{src}"></script>\n'.format(
                        src=compiled_js_path)
                    line = indent + script

                lines.append(line)

        with open(path, 'w') as f:
            for line in lines:
                f.write(line)

    def _build(self, builder_args, project_root):
        builder = self.config.closurebuilder()

        cmd = ['python', builder] + [str(arg) for arg in builder_args]

        popen_args = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE
        }

        builder_proc = subprocess.Popen(cmd, **popen_args)
        result = builder_proc.communicate()

        if builder_proc.returncode != 0:
            raise GoogkitError('Compilation failed:\n' + result[1].decode())
        else:
            logging.debug(result[1].decode())

    def build_debug(self, project_root):
        self.setup_files(self.config.debug_dir())

        logging.info('Building for debug...')
        args = self.debug_arguments(project_root)
        self._build(args, project_root)

        # The root path should be set by 'sourceRoot', but Closure Compiler
        # doesn't support this attribute.
        # So set 'sourceRoot' to 'project_root' directory manually until
        # Closure Compiler supports this feature.
        source_map = os.path.join(project_root,
                                  self.config.debug_dir(),
                                  self.config.compiled_js() + '.map')
        self.modify_source_map(source_map, project_root)

        logging.info('Done.')

    def build_production(self, project_root):
        self.setup_files(self.config.production_dir())

        logging.info('Building for production...')
        args = self.production_arguments(project_root)
        self._build(args, project_root)
        logging.info('Done.')

    def debug_arguments(self, project_root):
        config = self.config
        compiled_js = os.path.join(config.debug_dir(), config.compiled_js())
        source_map_path = compiled_js + '.map'
        source_map = os.path.basename(source_map_path)

        source_map_comment = '"%output%//# sourceMappingURL={path}"'.format(
            path=source_map)

        # The library path should be a relative path from the project root.
        # If '--root' is specified as absolute path, 'sources' attribute of
        # the source map will be absolute path and not work with http scheme.
        lib_path = os.path.relpath(config.library_root(), project_root)

        args = BuildCommand.BuilderArguments()
        args.builder_arg('--root', lib_path)
        args.builder_arg('--root', config.js_dev_dir())
        args.builder_arg('--namespace', 'main')
        args.builder_arg('--output_mode', 'compiled')
        args.builder_arg('--output_file', compiled_js)
        args.builder_arg('--compiler_jar', config.compiler())
        args.compiler_arg('--compilation_level', config.compilation_level())
        args.compiler_arg('--source_map_format', 'V3')
        args.compiler_arg('--create_source_map', source_map_path)
        args.compiler_arg('--output_wrapper', source_map_comment)
        return args

    def production_arguments(self, project_root):
        config = self.config
        compiled_js = os.path.join(config.production_dir(),
                                   config.compiled_js())
        lib_path = os.path.relpath(config.library_root(), project_root)

        args = BuildCommand.BuilderArguments()
        args.builder_arg('--root', lib_path)
        args.builder_arg('--root', config.js_dev_dir())
        args.builder_arg('--namespace', 'main')
        args.builder_arg('--output_mode', 'compiled')
        args.builder_arg('--output_file', compiled_js)
        args.builder_arg('--compiler_jar', config.compiler())
        args.compiler_arg('--compilation_level', config.compilation_level())
        args.compiler_arg('--define', 'goog.DEBUG=false')
        return args

    def modify_source_map(self, source_map, project_root):
        source_root = os.path.relpath(project_root, self.config.debug_dir())

        with open(source_map) as source_map_file:
            source_map_content = json.load(source_map_file)
            source_map_content['sourceRoot'] = source_root

        with open(source_map, 'w') as source_map_file:
            json.dump(source_map_content, source_map_file)

    def run_internal(self):
        project_root = googkit.lib.path.project_root(self.env.cwd)
        with working_directory(project_root):
            if self.env.argument.option('--debug'):
                self.build_debug(project_root)
                return

            if self.config.is_debug_enabled():
                self.build_debug(project_root)
            self.build_production(project_root)
