import os
from googkit.lib.error import GoogkitError


PROJECT_CONFIG = 'googkit.cfg'
USER_CONFIG = '.googkit'
DEFAULT_CONFIG = os.path.join('googkit_data', 'default.cfg')
SCRIPT_DIR = 'googkit'
PLUGIN_DIR = 'plugins'
TEMPLATE_DIR = os.path.join('googkit_data', 'template')


def googkit_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, '..', '..'))


def project_root(cwd):
    current = cwd
    try:
        while not os.path.exists(os.path.join(current, PROJECT_CONFIG)):
            before = current
            current = os.path.dirname(current)

            # Break if current smeems root.
            if before == current:
                break

        if os.path.exists(os.path.join(current, PROJECT_CONFIG)):
            return current
        else:
            return None
    except IOError:
        return None


def project_config(cwd):
    proj_root = project_root(cwd)

    if proj_root is None:
        raise GoogkitError('Project directory is not found.')

    project_config = os.path.join(proj_root, PROJECT_CONFIG)

    if not os.path.exists(project_config):
        raise GoogkitError('Project config file is not found.')

    return project_config


def user_config():
    home_dir = os.path.expanduser('~')
    user_config = os.path.join(home_dir, USER_CONFIG)

    return user_config if os.path.exists(user_config) else None


def default_config():
    path = os.path.join(googkit_root(), DEFAULT_CONFIG)
    if not os.path.exists(path):
        msg = 'Default config file is not found: {path}'.format(path=path)
        raise GoogkitError(msg)

    return path


def plugin():
    plugin_dir = os.path.join(googkit_root(), SCRIPT_DIR, PLUGIN_DIR)
    if not os.path.isdir(plugin_dir):
        msg = 'Plugins directory is not found: {path}'.format(path=plugin_dir)
        raise GoogkitError(msg)

    return plugin_dir


def template():
    template_dir = os.path.join(googkit_root(), TEMPLATE_DIR)
    if not os.path.isdir(template_dir):
        msg = 'Template directory is not found: {path}'.format(path=template_dir)
        raise GoogkitError(msg)

    return template_dir
