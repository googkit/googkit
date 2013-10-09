import sys
import urllib

_urllib = None

if hasattr(urllib, 'urlretrieve'):
    # Python 2.x
    _urllib = urllib
else:
    # Python 3.x or later
    import urllib.request
    _urllib = urllib.request


def run(url, target_path):
    _urllib.urlretrieve(url, target_path)
