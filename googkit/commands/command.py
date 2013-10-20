import logging
import os
import googkit.lib.path
from googkit.lib.config import Config
from googkit.lib.error import GoogkitError
from googkit.lib.error import InvalidOptionError
from googkit.lib.logutil import log_level


class Command(object):
    def __init__(self, env):
        self.env = env

    @classmethod
    def needs_project_config(cls):
        return False

    @classmethod
    def supported_options(cls):
        return set(['--verbose'])

    def _validate_options(self):
        opts = set(self.env.argument.options.keys())
        unsupported_opts = opts - self.__class__.supported_options()

        if len(unsupported_opts) > 0:
            raise InvalidOptionError(unsupported_opts)

    def _load_config(self):
        default_config = googkit.lib.path.default_config()
        user_config = googkit.lib.path.user_config()
        project_config = googkit.lib.path.project_config(self.env.cwd)

        if project_config is None:
            raise GoogkitError('No config file found.')

        config = Config()
        config.load(project_config, user_config, default_config)
        return config

    def _setup(self):
        if self.__class__.needs_project_config():
            self.config = self._load_config()
        else:
            self.config = None

        os.chdir(self.env.cwd)

    def run(self):
        level = logging.DEBUG if self.env.argument.option('--verbose') else None
        with log_level(level):
            self._validate_options()
            self._setup()
            self.run_internal()

    def run_internal(self):
        pass
