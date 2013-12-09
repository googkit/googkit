import glob
import logging
import os.path
import subprocess
import googkit.lib.path
from googkit.commands.command import Command
from googkit.lib.argument_builder import ArgumentBuilder
from googkit.lib.dirutil import working_directory
from googkit.lib.error import GoogkitError
from googkit.lib.i18n import _


class LintCommand(Command):
    @classmethod
    def needs_project_config(cls):
        return True

    def _sources(self):
        js_dev = self.config.js_dev_dir()
        deps_js = self.config.deps_js()

        pattern = os.path.join(js_dev, '*.js')
        paths = glob.glob(pattern)

        if deps_js in paths:
            paths.remove(deps_js)
        return paths

    def lint(self):
        if googkit.lib.file.which('gjslint') is None:
            raise GoogkitError(_('Required command not found: gjslint'))

        paths = self._sources()
        args = ArgumentBuilder()

        flagfile = self.config.linter_flagfile()
        if os.path.exists(flagfile):
            args.add('--flagfile', flagfile)

        cmd = ['gjslint'] + [str(arg) for arg in args] + paths

        popen_args = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE
        }

        proc = subprocess.Popen(cmd, **popen_args)
        result = proc.communicate()

        logging.info(result[0].decode())

    def run_internal(self):
        project_root = googkit.lib.path.project_root(self.env.cwd)
        with working_directory(project_root):
            self.lint()
