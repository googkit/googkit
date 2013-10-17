import os


class CurrentDirectory(object):
    """Context manager for changing the current working directory.

    :param path: Path of the working directory where move to.
    """
    def __init__(self, path):
        self._cwd = path
        self._priv_cwd = os.getcwd()

    def __enter__(self):
        os.chdir(self._cwd)

    def __exit__(self, *args):
        os.chdir(self._priv_cwd)


def working_directory(path='.'):
    """Change current working directory.

    :param path: Path of the working directory where move to.
    :returns: `CurrentDirectory` as a context manager

    >>> import tempfile
    >>> import os.path
    >>> base = os.getcwd()
    >>> temp = tempfile.mkdtemp()
    >>> with working_directory(temp):
    ...     assert os.path.samefile(os.getcwd(), temp)
    ...
    >>> assert os.path.samefile(os.getcwd(), base)
    """
    return CurrentDirectory(path)
