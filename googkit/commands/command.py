import logging
import os
import googkit.lib.path
from googkit.lib.config import Config
from googkit.lib.error import GoogkitError
from googkit.lib.error import InvalidOptionError
from googkit.lib.i18n import _
from googkit.lib.logutil import log_level


class Command(object):
    """A base class for commands.
    """

    def __init__(self, env):
        """Create a command that depend the specified environment.
        """
        self.env = env

    @classmethod
    def needs_project_config(cls):
        """Whether this command depend to a project config file.
        You should override to return True if this command use a project
        config.
        """
        return False

    @classmethod
    def supported_options(cls):
        """Returns a set has supported options by this command.
        In default, all command should support a --verbose option to display
        verbose messages.
        """
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
            raise GoogkitError(_('No config file found.'))

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
        """Runs this command.
        Override run_internal instead of run if you want to implement a new
        command.
        """
        level = logging.DEBUG if self.env.argument.option('--verbose') else None
        with log_level(level):
            self._validate_options()
            self._setup()
            self.run_internal()

    def run_internal(self):
        """Internal method for running command.
        You can change a command behavior by overriding this method.
        """
        pass
