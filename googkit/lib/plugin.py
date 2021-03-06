import os
import googkit.lib.path
from googkit.lib.error import GoogkitError
from googkit.lib.i18n import _


INIT_FILE = '__init__.py'
COMMAND_FILE = 'command.py'


def load(tree):
    """Loads googkit plugins to the specified instance of CommandTree.
    """
    base_dir = googkit.lib.path.plugin()

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

        module_name = 'plugins.{filename}.command'.format(filename=filename)
        module = __import__(module_name, fromlist=['command'])
        if not hasattr(module, 'register'):
            raise GoogkitError(_('No register method found for plugin: {module}').format(
                module=module_name))

        module.register(tree)
