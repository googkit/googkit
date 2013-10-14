import logging
import os
import re
from googkit.commands.command import Command


class ApplyConfigCommand(Command):
    CONFIG_TARGET_EXT = ('.html', '.xhtml', '.js', '.css')

    def __init__(self, env):
        super(ApplyConfigCommand, self).__init__(env)

    @classmethod
    def needs_config(cls):
        return True

    @classmethod
    def line_indent(cls, line):
        indent = ''
        m = re.search(r'^(\s*)', line)
        if len(m.groups()) >= 1:
            indent = m.group(1)

        return indent

    @classmethod
    def html_path(cls, path):
        return '/'.join(path.split(os.sep))

    def update_base_js(self, line, dirpath):
        path = self.env.config.base_js()
        relpath = os.path.relpath(path, dirpath)

        return '<script type="text/javascript" src="{href}"></script>'.format(href=ApplyConfigCommand.html_path(relpath))

    def update_deps_js(self, line, dirpath):
        path = self.env.config.deps_js()
        relpath = os.path.relpath(path, dirpath)

        return '<script type="text/javascript" src="{src}"></script>'.format(src=ApplyConfigCommand.html_path(relpath))

    def update_multitestrunner_css(self, line, dirpath):
        path = self.env.config.multitestrunner_css()
        relpath = os.path.relpath(path, dirpath)

        return '<link rel="stylesheet" type="text/css" href="{href}">'.format(href=ApplyConfigCommand.html_path(relpath))

    def apply_config(self, path):
        lines = []
        updaters = {
            '<!--@base_js@-->': self.update_base_js,
            '<!--@deps_js@-->': self.update_deps_js,
            '<!--@multitestrunner_css@-->': self.update_multitestrunner_css}
        markers = updaters.keys()
        dirpath = os.path.dirname(path)

        with open(path) as fp:
            for line in fp:
                for marker in markers:
                    if line.find(marker) >= 0:
                        logging.debug('Applying config to {path} ...'.format(path=path))
                        updater = updaters[marker]
                        line = ApplyConfigCommand.line_indent(line) + updater(line, dirpath) + marker + '\n'
                lines.append(line)

        with open(path, 'w') as fp:
            for line in lines:
                fp.write(line)

    def apply_config_all(self):
        devel_dir = self.env.config.development_dir()

        # If library_root is in development_dir, we should avoid to walk into the library_root.
        ignores = (
            self.env.config.library_root(),
            self.env.config.compiler_root())

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
        logging.info('Applying config...')
        self.apply_config_all()
