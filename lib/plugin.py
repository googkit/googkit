import os
import lib.path


PLUGIN_DIR = 'plugins'
INIT_FILE = '__init__.py'
COMMAND_FILE = 'command.py'


def load(tree):
    base_dir = os.path.join(path.googkit_root(), PLUGIN_DIR)

    for filename in os.listdir(base_dir):
        plugin_dir = os.path.join(base_dir, filename)
        if not os.path.isdir(plugin_dir):
            continue

        init_path = os.path.join(plugin_dir, INIT_FILE)
        if not os.path.exists(init_path):
            continue

        command_path = os.path.join(plugin_dir, COMMAND_FILE)
        if not os.path.exists(command_path):
            continue

        module = __import__('plugins.%s.command' % (filename), fromlist=['command'])
        if not hasattr(module, 'register'):
            continue

        module.register(tree)
