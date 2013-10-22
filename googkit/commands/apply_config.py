import logging
import os
import re
import googkit.lib.path
import googkit.compat.urllib.request
from googkit.lib.dirutil import working_directory
from googkit.commands.command import Command


class ApplyConfigCommand(Command):
    CONFIG_TARGET_EXT = ('.html', '.xhtml', '.js', '.css')

    @classmethod
    def needs_project_config(cls):
        return True

    @classmethod
    def line_indent(cls, line):
        indent = ''
        m = re.search(r'^(\s*)', line)
        if len(m.groups()) >= 1:
            indent = m.group(1)

        return indent

    def update_base_js(self, line, dirpath):
        path = self.config.base_js()
        relpath = os.path.relpath(path, dirpath)
        href = googkit.compat.urllib.request.pathname2url(relpath)

        return '<script src="{href}"></script>'.format(href=href)

    def update_deps_js(self, line, dirpath):
        path = self.config.deps_js()
        relpath = os.path.relpath(path, dirpath)
        src = googkit.compat.urllib.request.pathname2url(relpath)

        return '<script src="{src}"></script>'.format(src=src)

    def update_multitestrunner_css(self, line, dirpath):
        path = self.config.multitestrunner_css()
        relpath = os.path.relpath(path, dirpath)
        href = googkit.compat.urllib.request.pathname2url(relpath)

        return '<link rel="stylesheet" href="{href}">'.format(href=href)

    def apply_config(self, path):
        lines = []
        updaters = {
            'base.js': {'marker': '<!--@base_js@-->', 'update': self.update_base_js},
            'deps.js': {'marker': '<!--@deps_js@-->', 'update': self.update_deps_js},
            'multitestrunner.css': {'marker': '<!--@multitestrunner_css@-->', 'update': self.update_multitestrunner_css}
        }
        dirpath = os.path.dirname(path)

        with open(path) as fp:
            for line in fp:
                for updater_name in updaters.keys():
                    marker = updaters[updater_name]['marker']
                    update = updaters[updater_name]['update']
                    if line.find(marker) >= 0:
                        msg = 'Replaced a {name} path on {path}'.format(name=updater_name, path=path)
                        logging.debug(msg)

                        line = '{indent}{content}{marker}\n'.format(
                            indent=ApplyConfigCommand.line_indent(line),
                            content=update(line, dirpath),
                            marker=marker)

                lines.append(line)

        with open(path, 'w') as fp:
            for line in lines:
                fp.write(line)

    def apply_config_all(self):
        devel_dir = self.config.development_dir()

        # If library_root is in development_dir, we should avoid to walk into the library_root.
        ignores = (
            self.config.library_root(),
            self.config.compiler_root())

        for root, dirs, files in os.walk(devel_dir):
            for filename in files:
                (base, ext) = os.path.splitext(filename)
                if ext not in ApplyConfigCommand.CONFIG_TARGET_EXT:
                    continue

                filepath = os.path.join(root, filename)
                self.apply_config(filepath)

            # Avoid to walk into ignores
            for dirname in dirs:
                if os.path.join(root, dirname) in ignores:
                    dirs.remove(dirname)

    def run_internal(self):
        project_root = googkit.lib.path.project_root(self.env.cwd)
        with working_directory(project_root):
            self.apply_config_all()
        logging.info('Applied configs.')
