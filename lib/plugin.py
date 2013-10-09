import os
import path


PLUGIN_DIR = 'plugin'


def load(tree):
    dir = os.path.join(path.googkit_root(), PLUGIN_DIR)

    for filename in os.listdir(dir):
        (base, ext) = os.path.splitext(filename)
        if base == '__init__':
            continue
        if ext != '.py':
            continue

        module = __import__('plugin.' + base, fromlist=[base])
        if not hasattr(module, 'register'):
            continue

        module.register(tree)
