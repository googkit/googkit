import distutils.core
import os
import shutil
from cmds.command import Command
from lib.error import GoogkitError


class InitCommand(Command):
    TEMPLATE_DIR = 'template'


    def __init__(self, env):
        super(InitCommand, self).__init__(env)


    def template_dir(self):
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        template_dir = os.path.join(script_dir, InitCommand.TEMPLATE_DIR)
        return template_dir


    def copy_template(self, dst_dir):
        template_dir = self.template_dir()

        if os.listdir(dst_dir):
            raise GoogkitError('Directory is not empty: ' + dst_dir)

        distutils.dir_util.copy_tree(template_dir, dst_dir)


    def run_internal(self):
        self.copy_template(os.getcwd())