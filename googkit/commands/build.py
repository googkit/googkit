import glob
import json
import logging
import os
import os.path
import re
import shutil
import subprocess
import googkit.lib.file
import googkit.lib.path
import googkit.lib.strutil
from googkit.commands.command import Command
from googkit.lib.option_builder import OptionBuilder
from googkit.lib.dirutil import working_directory
from googkit.lib.error import GoogkitError
from googkit.lib.i18n import _


class BuildCommand(Command):
    """A class for build commands.
    """

    """Extension (like .html) tuple to compile.
    HTML: .html .htm
    XHTML: .xml .xhtml .xht
    """
    HTML_LIKE_EXT = ('.xml', '.xhtml', '.xht', '.htm', '.html')

    class BuilderArguments(OptionBuilder):
        """Argument builder for Closure Builder.

        Usage::
            >>> args = BuildCommand.BuilderArguments()
            >>> args.builder_arg('--arg1', 'VAL1')
            >>> args.builder_arg('--arg2', 'VAL2')
            >>> args.compiler_arg('--arg3', 'VAL3')
            >>> str(args)
            '--arg1=VAL1 --arg2=VAL2 --compiler_flags=--arg3=VAL3'
        """

        def builder_arg(self, key, value):
            """Adds an argument for Closure Builder.

            Usage::
                >>> args = BuildCommand.BuilderArguments()
                >>> args.builder_arg('--arg', 'VAL')
                >>> str(args)
                '--arg=VAL'
            """
            self.add(key, value)

        def compiler_arg(self, key, value):
            """Adds an argument for Closure Compiler.

            Usage::
                >>> args = BuildCommand.BuilderArguments()
                >>> args.compiler_arg('--arg', 'VAL')
                >>> str(args)
                '--compiler_flags=--arg=VAL'
            """
            self.add('--compiler_flags', '{0}={1}'.format(key, value))

    @classmethod
    def needs_project_config(cls):
        return True

    @classmethod
    def supported_options(cls):
        opts = super(BuildCommand, cls).supported_options()
        opts.add('--clean')
        opts.add('--debug')
        return opts

    @classmethod
    def ignore_dirs(cls, *ignore_dirs):
        """Returns a callable ignore argument for copytree method by the
        specified ignore directories.
        """
        def ignoref(dirpath, files):
            return [filename for filename in files
                    if (os.path.join(dirpath, filename) in ignore_dirs)]
        return ignoref

    def setup_files(self, target_dir, should_clean=False):
        """Copy project resources to the specified directory path.
        Removes files already exist in the target directory if should_clean is
        True.
        """
        config = self.config
        devel_dir = config.development_dir()

        # Avoid to copy unnecessary files for production
        ignores = (
            config.testrunner(),
            config.library_root(),
            config.compiler_root(),
            config.js_dev_dir())

        if should_clean:
            shutil.rmtree(target_dir)

        googkit.lib.file.copytree(
            devel_dir,
            target_dir,
            ignore=BuildCommand.ignore_dirs(*ignores))

        for root, dirs, files in os.walk(target_dir):
            for filename in files:
                html_path = os.path.join(root, filename)
                (base, ext) = os.path.splitext(html_path)
                if ext not in BuildCommand.HTML_LIKE_EXT:
                    continue

                self.compile_resource(html_path)

    def compile_resource(self, html_path):
        """Converts development resources for production resources.
        For example, paths for development resources will be replaced by paths
        for compiled resources.
        """
        lines = []

        with open(html_path) as f:
            for line in f:
                # Remove lines that requires unneeded scripts
                if line.find('<!--@base_js@-->') >= 0:
                    continue
                if line.find('<!--@deps_js@-->') >= 0:
                    continue

                # Replace deps.js by a compiled script
                if line.find('<!--@require_main@-->') >= 0:
                    indent = googkit.lib.strutil.line_indent(line)
                    compiled_js_path = os.path.relpath(
                        self.compiled_js_path(html_path), os.path.dirname(html_path))
                    script = '<script src="{src}"></script>\n'.format(src=compiled_js_path)
                    line = indent + script

                lines.append(line)

        with open(html_path, 'w') as f:
            for line in lines:
                f.write(line)

    def namespace_by_html(self, html_path):
        """Returns a namespace key for main scripts by a path of the HTML.
        For example, returns `googkit.hoge` if the path is `hoge.html`.
        """
        filename = os.path.splitext(os.path.basename(html_path))[0]
        return 'googkit_{0}'.format(filename)

    def compiled_js_path(self, html_path):
        """Returns a compiled js path by a path of the HTML.
        For example, returns `foo/bar.min.js` if the path is `foo/bar.html`.
        """
        ext_pattern = self.config.compiled_js_ext()
        return ext_pattern.replace('%s', os.path.splitext(html_path)[0])

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
            raise GoogkitError(_('Compilation failed:\n{message}').format(
                message=result[1].decode()))
        else:
            logging.debug(result[1].decode())

    def html_requiring_js(self):
        """Returns path list of HTMLs requiring built JavaScript.
        """
        config = self.config
        devel_dir = config.development_dir()

        html_glob = os.path.join(devel_dir, '*.html')
        htm_glob = os.path.join(devel_dir, '*.htm')
        html_list = glob.glob(html_glob) + glob.glob(htm_glob)
        testrunner = config.testrunner()

        return filter(lambda path: path != testrunner, html_list)

    def build_debug(self, html_path, project_root, should_clean=False):
        """Builds resources is in the specified project root for debugging.
        Removes old resources if should_clean is True.
        """
        config = self.config
        self.setup_files(config.debug_dir(), should_clean)

        logging.info(_('Building for debug: ') + html_path)
        args = self.debug_arguments(html_path, project_root)
        self._build(args, project_root)

        # The root path should be set by 'sourceRoot', but Closure Compiler
        # doesn't support this attribute.
        # So set 'sourceRoot' to 'project_root' directory manually until
        # Closure Compiler supports this feature.
        html_relpath = os.path.relpath(html_path, config.development_dir())
        debug_html_path = os.path.join(config.debug_dir(), html_relpath)
        compiled_js_path = self.compiled_js_path(debug_html_path)
        source_map_path = compiled_js_path + '.map'

        self.modify_source_map(source_map_path, project_root)

        logging.info(_('Done.'))

    def build_production(self, html_path, project_root, should_clean=False):
        """Builds resources is in the specified project root for production.
        Removes old resources if should_clean is True.
        """
        config = self.config
        self.setup_files(config.production_dir(), should_clean)

        logging.info(_('Building for production: ' + html_path))
        args = self.production_arguments(html_path, project_root)
        self._build(args, project_root)
        logging.info(_('Done.'))

    def debug_arguments(self, html_path, project_root):
        """Returns an arguments for Closure Compiler to build debugging.
        This arguments created for each HTML requiring JavaScript.
        """
        config = self.config
        html_relpath = os.path.relpath(html_path, config.development_dir())
        debug_html_path = os.path.join(config.debug_dir(), html_relpath)
        compiled_js_path = self.compiled_js_path(debug_html_path)
        source_map_path = compiled_js_path + '.map'
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
        args.builder_arg('--namespace', self.namespace_by_html(html_path))
        args.builder_arg('--output_mode', 'compiled')
        args.builder_arg('--output_file', compiled_js_path)
        args.builder_arg('--compiler_jar', config.compiler())
        args.compiler_arg('--compilation_level', config.compilation_level())
        args.compiler_arg('--source_map_format', 'V3')
        args.compiler_arg('--create_source_map', source_map_path)
        args.compiler_arg('--output_wrapper', source_map_comment)

        flagfile = config.compiler_flagfile_for_debug()
        if os.path.exists(flagfile):
            args.compiler_arg('--flagfile', flagfile)
        return args

    def production_arguments(self, html_path, project_root):
        """Returns an arguments for Closure Compiler to build production.
        This arguments created for each HTML requiring JavaScript.
        """
        config = self.config
        html_relpath = os.path.relpath(html_path, config.development_dir())
        production_html_path = os.path.join(config.production_dir(), html_relpath)
        compiled_js_path = self.compiled_js_path(production_html_path)
        lib_path = os.path.relpath(config.library_root(), project_root)

        args = BuildCommand.BuilderArguments()
        args.builder_arg('--root', lib_path)
        args.builder_arg('--root', config.js_dev_dir())
        args.builder_arg('--namespace', self.namespace_by_html(html_path))
        args.builder_arg('--output_mode', 'compiled')
        args.builder_arg('--output_file', compiled_js_path)
        args.builder_arg('--compiler_jar', config.compiler())
        args.compiler_arg('--compilation_level', config.compilation_level())
        args.compiler_arg('--define', 'goog.DEBUG=false')

        flagfile = config.compiler_flagfile()
        if os.path.exists(flagfile):
            args.compiler_arg('--flagfile', flagfile)
        return args

    def modify_source_map(self, source_map, project_root):
        """ Modifies library paths in the source map.
        The library path should be a relative path from the project root.
        If '--root' is specified as absolute path, 'sources' attribute of the
        source map will be absolute path and not work with http scheme.
        """
        source_root = os.path.relpath(project_root, self.config.debug_dir())

        with open(source_map) as source_map_file:
            source_map_content = json.load(source_map_file)
            source_map_content['sourceRoot'] = source_root

        with open(source_map, 'w') as source_map_file:
            json.dump(source_map_content, source_map_file)

    def run_internal(self):
        project_root = googkit.lib.path.project_root(self.env.cwd)
        with working_directory(project_root):
            should_clean = self.env.argument.option('--clean')

            for html_path in self.html_requiring_js():
                if self.env.argument.option('--debug'):
                    self.build_debug(html_path, project_root, should_clean)
                else:
                    self.build_production(html_path, project_root, should_clean)
