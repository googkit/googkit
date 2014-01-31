import os


class CurrentDirectory(object):
    """Context manager for changing the current working directory.
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
