import re
import os

ParserClass = None
try:
    # Python 2.x
    import ConfigParser
    ParserClass = ConfigParser.ConfigParser
except ImportError:
    # Python 3.x or later
    import configparser
    ParserClass = configparser.ConfigParser


class GlobalConfig(object):
    DEFAULT_CONFIG = ''
    def __init__(self):
        pass

    def load(self, default_path, user_path = None):
        parser = ParserClass()

        with open(default_path) as f:
            parser.readfp(f)

        if user_path is not None:
            with open(user_path) as f:
                parser.readfp(f)

        self.parser = parser


    def library_root(self):
        path = self.parser.get('library', 'root')
        return os.path.normpath(path)


    def compiler_root(self):
        path = self.parser.get('compiler', 'root')
        return os.path.normpath(path)
