import sys

urllib_urlretrieve = None
try:
    # Python 2.x
    import urllib
    urllib_urlretrieve = urllib.urlretrieve
except ImportError:
    # Python 3.x or later
    import urllib.request
    urllib_urlretrieve = urllib.request.urlretrieve


def run(url, target_path):
    urllib_urlretrieve(url, target_path)
