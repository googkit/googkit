import sys

_urllib = None
try:
    # Python 2.x
    import urllib
    urllib.urlretrieve
    _urllib = urllib
except ImportError:
    # Python 3.x or later
    import urllib.request
    _urllib = urllib.request


def run(url, target_path):
    _urllib.urlretrieve(url, target_path)
