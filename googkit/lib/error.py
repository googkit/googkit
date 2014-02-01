class GoogkitError(Exception):
    """Base class for error in Googkit."""

    def __init__(self, message):
        # TODO: Add docstirng.
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.message


class InvalidOptionError(GoogkitError):
    """Raised when detecting invalid options."""

    def __init__(self, options):
        # TODO: Add docstirng.
        self._options = options
        message = 'Invalid option: {options}'.format(
            options=', '.join(self._options))
        super(InvalidOptionError, self).__init__(message)

    @property
    def options(self):
        # TODO: Add docstirng.
        return self._options
