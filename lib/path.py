import os
import os.path
from lib.error import GoogkitError


PROJECT_CONFIG = 'googkit.cfg'
USER_CONFIG = '.googkit'
GOOGKIT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DEFAULT_CONFIG = os.path.join(GOOGKIT_ROOT, 'config', 'default.cfg')


def googkit_root():
    return GOOGKIT_ROOT


def project_root():
    current = os.getcwd()
    try:
        while not os.path.exists(os.path.join(current, PROJECT_CONFIG)):
            before = current
            current = os.path.abspath(os.path.join(current, '../'))

            # Break if current smeems root.
            if before == current:
                break

        if os.path.exists(os.path.join(current, PROJECT_CONFIG)):
            return current
        else:
            return None
    except IOError:
        return None


def project_config():
    proj_root = project_root()

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
    if not os.path.exists(DEFAULT_CONFIG):
        raise GoogkitError('Default config file is not found: %s' % default_config)

    return DEFAULT_CONFIG
