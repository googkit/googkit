import distutils.core
import os
import shutil
from lib.error import GoogkitError


class InitCommand(object):
    TEMPLATE_DIR = 'template'


    def __init__(self, config):
        pass


    def copy_template(self, dst_dir):
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        template_dir = os.path.join(script_dir, InitCommand.TEMPLATE_DIR)

        if os.listdir(dst_dir):
            raise GoogkitError('Directory is not empty: ' + dst_dir)

        distutils.dir_util.copy_tree(template_dir, dst_dir)


    def run(self):
        self.copy_template(os.getcwd())
        print('Initialization completed.')
