#!/usr/bin/env python


import sys

urllib_urlretrieve = None
try:
    # Python 3.x or later
    import urllib.request
    urllib_urlretrieve = urllib.request.urlretrieve
except ImportError:
    # Python 2.x
    import urllib
    urllib_urlretrieve = urllib.urlretrieve


def download(url, target_path):
    urllib_urlretrieve(url, target_path)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s url target_path' % sys.argv[0]
        sys.exit()

    url = sys.argv[1]
    target_path = sys.argv[2]
    download(url, target_path)
