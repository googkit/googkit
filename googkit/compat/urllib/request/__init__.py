import urllib


if not hasattr(urllib, 'urlretrieve'):
    # 3.0 and later
    import urllib.request
    urlretrieve = urllib.request.urlretrieve
else:
    urlretrieve = urllib.urlretrieve


if not hasattr(urllib, 'pathname2url'):
    import urllib.request
    pathname2url = urllib.request.pathname2url
else:
    pathname2url = urllib.pathname2url
