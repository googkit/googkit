import logging
import os
import googkit.lib.path
from googkit.lib.config import Config
from googkit.lib.error import GoogkitError


class Command(object):
    def __init__(self, env):
        self.env = env

    # TODO: Rename: needs_project_config
    @classmethod
    def needs_config(cls):
        return False

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
        if self.__class__.needs_config():
            self.config = self._load_config()
        else:
            self.config = None

        os.chdir(self.env.cwd)

    def run(self):
        self._setup()
        self.run_internal()
        self.complete()

    def run_internal(self):
        # Override the method to implement a behavior
        pass

    def complete(self):
        logging.info('Complete.')
