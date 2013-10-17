import logging


class LogLevelChanger(object):
    """Log level changer for with-statements.

    This class temporarily changes a log level of the specified logger in a `with` statement.
    You can get the logger by `as` clause.

    :param level: Log level used in this context.
    :param logger_name: Name of the logger will be changed the level.

    Usage::
        >>> logger = logging.getLogger('test')
        >>> logger.setLevel(logging.INFO)
        >>> with LogLevelChanger(logging.DEBUG, logger):
        ...     assert logger.level == logging.DEBUG
        ...
        >>> assert logger.level == logging.INFO
    """
    def __init__(self, level, logger):
        self.logger = logger
        self.level = level

    def __enter__(self):
        self._orig_level = self.logger.level
        self.logger.setLevel(self.level)
        return self.logger

    def __exit__(self, *args):
        self.logger.setLevel(self._orig_level)


def log_level(level=None, logger=None):
    """Change log level.

    This class temporarily changes a log level of the specified logger in a `with` statement.
    You can get the logger by `as` clause.

    :param level: Log level used in this context (do not change the level, if None).
    :param logger_name: Name of the logger will be changed the level (root logger, if None).
    :returns: `LogLevelChanger` as a context manager.

    Usage::
        >>> with log_level(logging.DEBUG) as logger:
        ...     assert logger.level == logging.DEBUG
        ...
        >>> assert logger.level == logging.WARNING
    """
    if logger is not None:
        logger_ = logger
    else:
        logger_ = logging.getLogger()

    if level is not None:
        level_ = level
    else:
        level_ = logger_.level

    return LogLevelChanger(level_, logger_)
