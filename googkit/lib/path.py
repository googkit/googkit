import os
from googkit.lib.error import GoogkitError


PROJECT_CONFIG = 'googkit.cfg'
DATA_DIR = 'googkit_data'
USER_CONFIG = '.googkit'
SCRIPT_DIR = 'googkit'
PLUGIN_DIR = 'plugins'
LOCALE_DIR = os.path.join(DATA_DIR, 'locale')
DEFAULT_CONFIG = os.path.join(DATA_DIR, 'default.cfg')
TEMPLATE_DIR = os.path.join(DATA_DIR, 'template')


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


def locale():
    locale_dir = os.path.join(googkit_root(), LOCALE_DIR)

    if not os.path.isdir(locale_dir):
        msg = 'Locale directory is not found: {path}'.format(path=locale_dir)
        raise GoogkitError(msg)

    return locale_dir


def replace_base(target, old_base, new_base):
    """Replace a base directory in the target path with the new one."""
    prefix = os.path.commonprefix([target, old_base])
    diff = target[len(prefix) + 1:]
    return os.path.join(new_base, diff)
