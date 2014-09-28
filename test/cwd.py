import os
from pathlib import Path


class chdir:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = Path(newPath)

    def __enter__(self):
        self.savedPath = Path.cwd()
        os.chdir(str(self.newPath))

    def __exit__(self, etype, value, traceback):
        os.chdir(str(self.savedPath))
