class GoogkitError(Exception):
    """Base class for error in Googkit."""

    def __init__(self, message):
        """Creates a local error of googkit by the specified message.
        """
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.message


class InvalidOptionError(GoogkitError):
    """Raised when detecting invalid options."""

    def __init__(self, options):
        """Creates an invalid option error by the invalid option names.
        """
        self._options = options
        message = 'Invalid option: {options}'.format(
            options=', '.join(self._options))
        super(InvalidOptionError, self).__init__(message)

    @property
    def options(self):
        """Returns invalid options of the error cause.
        """
        return self._options
