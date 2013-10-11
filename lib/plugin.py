import os
import lib.path
from lib.error import GoogkitError


INIT_FILE = '__init__.py'
COMMAND_FILE = 'command.py'


def load(tree):
    base_dir = lib.path.plugin()

    for filename in os.listdir(base_dir):
        plugin_dir = os.path.join(base_dir, filename)

        if not os.path.isdir(plugin_dir):
            continue

        init_path = os.path.join(plugin_dir, INIT_FILE)
        if not os.path.exists(init_path):
            raise GoogkitError('{init_path} is not found.'.format(init_path=init_path))

        command_path = os.path.join(plugin_dir, COMMAND_FILE)
        if not os.path.exists(command_path):
            continue

        module_name = 'plugins.{filename}.command'.format(filename=filename)
        module = __import__(module_name, fromlist=['command'])
        if not hasattr(module, 'register'):
            msg = 'Invalid plugin {module_name} do not have register method.'.format(
                    module_name=module_name)
            raise GoogkitError(msg)

        module.register(tree)
