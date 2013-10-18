import urllib


if not hasattr(urllib, 'urlretrieve'):
    # 3.0 and later
    import urllib.request
    urlretrieve = urllib.request.urlretrieve
else:
    urlretrieve = urllib.urlretrieve
