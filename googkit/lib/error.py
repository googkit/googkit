class GoogkitError(Exception):
    """Base class for error in Googkit."""

    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.message


class InvalidOptionError(GoogkitError):
    """Raised when detecting invalid options."""

    def __init__(self, options):
        self._options = options
        message = 'Invalid option: ' + ', '.join(self._options)
        super(InvalidOptionError, self).__init__(message)

    @property
    def options(self):
        return self._options
