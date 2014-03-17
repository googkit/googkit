import glob
import logging
import os
import shutil
import googkit.compat.urllib.request
import googkit.lib.path
import googkit.lib.strutil
from googkit.commands.command import Command
from googkit.lib.dirutil import working_directory
from googkit.lib.i18n import _


class ApplyConfigCommand(Command):
    """A class for commands that apply config.
    """

    """Extensions for HTML-like documents.
    HTML: .html .htm
    XHTML: .xml .xhtml .xht
    """
    HTML_LIKE_EXT = ('.xml', '.xhtml', '.xht', '.htm', '.html')

    """Extensions for files that include a marker to replace a line by config.
    HTML: .html .htm
    XHTML: .xml .xhtml .xht
    CSS: .css
    JavaScript: .js
    """
    CONFIG_TARGET_EXT = HTML_LIKE_EXT + ('.js', '.css')

    @classmethod
    def needs_project_config(cls):
        return True

    @classmethod
    def get_namespace_by_html(cls, path):
        """Returns a namespace from the path to the html.
        Namespace for the documents should be declared as ``googkit_{filename of the document}``.

        Usage::
            >>> ApplyConfigCommand.get_namespace_by_html('index.html')
            "googkit_index"
        """
        basename = os.path.splitext(os.path.basename(path))[0]
        namespace = 'googkit_{basename}'.format(basename=basename)
        return namespace

    @classmethod
    def get_namespace_by_main(cls, path):
        """Returns a namespace from the path to the main script.

        Usage::
            >>> ApplyConfigCommand.get_namespace_by_main('googkit_index.js')
            "googkit_index"
        """
        return os.path.splitext(os.path.basename(path))[0]

    def update_base_js(self, line, path):
        """Returns an updated line that marked by ``<!--@base_js@-->``.
        The line is contained in the file specified the path.
        """
        dirpath = os.path.dirname(path)
        base_js = self.config.base_js()
        relpath = os.path.relpath(base_js, dirpath)
        href = googkit.compat.urllib.request.pathname2url(relpath)

        return '<script src="{href}"></script>'.format(href=href)

    def update_deps_js(self, line, path):
        """Returns an updated line that marked by ``<!--@deps_js@-->``.
        The line is contained in the file specified the path.
        """
        dirpath = os.path.dirname(path)
        deps_js = self.config.deps_js()
        relpath = os.path.relpath(deps_js, dirpath)
        src = googkit.compat.urllib.request.pathname2url(relpath)

        return '<script src="{src}"></script>'.format(src=src)

    def update_multitestrunner_css(self, line, path):
        """Returns an updated line that marked by ``<!--@multitestrunner_css@-->``.
        The line is contained in the file specified the path.
        """
        dirpath = os.path.dirname(path)
        multitestrunner_css = self.config.multitestrunner_css()
        relpath = os.path.relpath(multitestrunner_css, dirpath)
        href = googkit.compat.urllib.request.pathname2url(relpath)

        return '<link rel="stylesheet" href="{href}">'.format(href=href)

    def update_require_main(self, line, path):
        """Returns an updated line that marked by ``<!--@require_main@-->``.
        The line is contained in the file specified the path.
        """
        namespace = self.get_namespace_by_html(path)
        return '<script> goog.require(\'{namespace}\'); </script>'.format(namespace=namespace)

    def update_provide_main(self, line, path):
        """Returns an updated line that marked by ``/*@provide_main@*/``.
        The line is contained in the file specified the path.
        """
        namespace = self.get_namespace_by_main(path)
        return 'goog.provide(\'{namespace}\');'.format(namespace=namespace)

    def apply_config(self, path):
        """Applies configurations to a file that the path point to.
        """
        lines = []
        updaters = {
            'base.js': {
                'marker': '<!--@base_js@-->',
                'update': self.update_base_js
            },
            'deps.js': {
                'marker': '<!--@deps_js@-->',
                'update': self.update_deps_js
            },
            'multitestrunner.css': {
                'marker': '<!--@multitestrunner_css@-->',
                'update': self.update_multitestrunner_css
            },
            'require_main': {
                'marker': '<!--@require_main@-->',
                'update': self.update_require_main
            },
            'provide_main': {
                'marker': '/*@provide_main@*/',
                'update': self.update_provide_main
            },
        }

        with open(path) as fp:
            for line in fp:
                for updater_name in updaters.keys():
                    marker = updaters[updater_name]['marker']
                    update = updaters[updater_name]['update']
                    if line.find(marker) >= 0:
                        msg = _('Replaced a {name} path on {path}').format(name=updater_name, path=path)
                        logging.debug(msg)

                        line = '{indent}{content}{marker}\n'.format(
                            indent=googkit.lib.strutil.line_indent(line),
                            content=update(line, path),
                            marker=marker)

                lines.append(line)

        with open(path, 'w') as fp:
            for line in lines:
                fp.write(line)

    def apply_config_all(self):
        """Applies configurations to files that is in a googkit project directory.
        """
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

    def setup_main_scripts(self):
        """Set-up a main scripts as an entry point for the user application.
        This script will be generated automatically under the rule:

        #. Search HTML-like documents into development/.
        #. Generate the namespace path from a filename of the document.
        #. Search scripts that are named ``{namespace}.js`` into js_dev/
        #. If some scripts are not found, generate the scripts.
        """
        config = self.config
        devel_dir = config.development_dir()

        html_list = []
        for ext in self.HTML_LIKE_EXT:
            html_list += glob.glob(os.path.join(devel_dir, '*' + ext))

        for html_path in html_list:
            if os.path.abspath(html_path) == os.path.abspath(config.testrunner()):
                continue

            basename = self.get_namespace_by_html(html_path) + '.js'
            script_path = os.path.join(config.js_dev_dir(), basename)

            if os.path.exists(script_path):
                logging.debug(_('Skip generating the entry point: {path}').format(path=script_path))
                continue

            main_script_template = os.path.join(
                googkit.lib.path.template(), 'development', 'js_dev', 'googkit_index.js')

            shutil.copyfile(main_script_template, script_path)
            logging.debug(_('Generate the entry point: {path}').format(path=script_path))

    def run_internal(self):
        project_root = googkit.lib.path.project_root(self.env.cwd)
        with working_directory(project_root):
            self.setup_main_scripts()
            self.apply_config_all()

        logging.info('Applied all configs.')
