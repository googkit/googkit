import glob
import logging
import os.path
import subprocess
import googkit.lib.path
from googkit.commands.command import Command
from googkit.lib.argument_builder import ArgumentBuilder
from googkit.lib.dirutil import working_directory


class LintCommand(Command):
    @classmethod
    def needs_project_config(cls):
        return True

    @classmethod
    def is_linter_installed(cls):
        popen_args = {
            'shell': True,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
        }

        try:
            subprocess.check_call(['gjslint', '--version'], **popen_args)
            return True
        except subprocess.CalledProcessError:
            return False

    def _sources(self):
        js_dev = self.config.js_dev_dir()
        deps_js = self.config.deps_js()

        pattern = os.path.join(js_dev, '*.js')
        paths = glob.glob(pattern)

        if deps_js in paths:
            paths.remove(deps_js)
        return paths

    def lint(self):
        paths = self._sources()
        args = ArgumentBuilder()

        flagfile = self.config.linter_flagfile()
        if os.path.exists(flagfile):
            args.add('--flagfile', flagfile)

        cmd = ['gjslint'] + [str(arg) for arg in args] + paths

        popen_args = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
        }

        proc = subprocess.Popen(cmd, **popen_args)
        result = proc.communicate()

        logging.info(result[0].decode())

    def run_internal(self):
        if not LintCommand.is_linter_installed():
            logging.error('[Error] Closure Linter is not found.\n' +
                          '\n' +
                          'Did you install Closure Linter?\n' +
                          'Try: sudo easy_install http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz')
            return

        project_root = googkit.lib.path.project_root(self.env.cwd)
        with working_directory(project_root):
            self.lint()
