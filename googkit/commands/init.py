import distutils.core
import logging
import os
import googkit.lib.path
from googkit.commands.command import Command
from googkit.lib.error import GoogkitError
from googkit.lib.i18n import _


class InitCommand(Command):
    def copy_template(self, dst_dir):
        # TODO: Add docstirng.
        template_dir = googkit.lib.path.template()

        conflicted = set(os.listdir(dst_dir)) & set(os.listdir(template_dir))
        if conflicted:
            raise GoogkitError(_('Conflicted files: {files}').format(
                files=', '.join(conflicted)))

        distutils.dir_util.copy_tree(template_dir, dst_dir)

    def run_internal(self):
        cwd = self.env.cwd
        self.copy_template(cwd)
        logging.info(_('Initialized googkit project in {path}').format(
            path=cwd))
