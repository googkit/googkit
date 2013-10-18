import googkit.compat.urllib.request as request


def run(url, target_path):
    request.urlretrieve(url, target_path)
