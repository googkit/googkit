import urllib

urllib_ = None

if hasattr(urllib, 'urlretrieve'):
    # Python 2.x
    urllib_ = urllib
else:
    # Python 3.x or later
    import urllib.request
    urllib_ = urllib.request


def run(url, target_path):
    urllib_.urlretrieve(url, target_path)
