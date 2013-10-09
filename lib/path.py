import os
from error import GoogkitError


PROJECT_CONFIG = 'googkit.cfg'
USER_CONFIG = '.googkit'
DEFAULT_CONFIG = 'config/default.cfg'


def googkit_root():
    googkit_home_path = os.environ.get('GOOGKIT_HOME')
    if googkit_home_path is None:
        raise GoogkitError('Missing environment variable: "GOOGKIT_HOME"')

    if not os.path.exists(googkit_home_path):
        raise GoogkitError('googkit directory is not found: %s' % googkit_home_path)

    return os.path.expanduser(googkit_home_path)


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
    googkit_home_path = googkit_root()
    default_config = os.path.join(googkit_home_path, DEFAULT_CONFIG)

    if not os.path.exists(default_config):
        raise GoogkitError('Default config file is not found: %s' % default_config)

    return default_config
