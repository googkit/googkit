try:
    # 3.0 and later
    from configparser import ConfigParser
    from configparser import NoSectionError
except ImportError:
    from ConfigParser import ConfigParser
    from ConfigParser import NoSectionError

# [review] - Is there a way to import all classes?
# [todo] - Treat ConfigParser#readfp/read_file
