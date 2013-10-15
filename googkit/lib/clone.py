import logging
import os
import subprocess
from googkit.lib.error import GoogkitError


def run(repos, target_path):
    if os.path.exists(target_path):
        _pull(repos, target_path)
    else:
        _clone(repos, target_path)


def _pull(repos, target_path):
    cwd = os.getcwd()
    os.chdir(target_path)

    try:
        args = ['git', 'pull']

        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = proc.communicate()

        if proc.returncode != 0:
            raise GoogkitError('Git pull failed: ' + result[1])

        logging.debug(result[0])
    finally:
        os.chdir(cwd)


def _clone(repos, target_path):
    args = ['git', 'clone', repos, target_path]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = proc.communicate()

    if proc.returncode != 0:
        raise GoogkitError('Git clone failed: ' + result[1])

    logging.debug(result[0])
