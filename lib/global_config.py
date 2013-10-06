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
    def __init__(self):
        pass

    def load(self, path):
        parser = ParserClass()

        with open(path) as f:
            parser.readfp(f)

        self.parser = parser

    def global_library_root(self):
        path = self.parser.get('library', 'root')
        return os.path.normpath(path)


    def global_compiler_root(self):
        path = self.parser.get('compiler', 'root')
        return os.path.normpath(path)
