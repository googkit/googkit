import logging
import os
import subprocess
from googkit.lib.error import GoogkitError
from googkit.compat.urllib import request


def run(repos, target_path):
    if os.path.exists(target_path):
        _pull(repos, target_path)
    else:
        _clone(repos, target_path)


def _git_cmd():
    if os.name == 'nt':
        return 'git.cmd'
    else:
        return 'git'


def _pull(repos, target_path):
    args = [_git_cmd(), 'pull']
    proc = subprocess.Popen(args, cwd=target_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = proc.communicate()

    if proc.returncode != 0:
        raise GoogkitError('Git pull failed: ' + result[1].decode())

    logging.debug(result[0].decode())


def _clone(repos, target_path):
    # git-clone on Windows expected unix-like path
    args = [_git_cmd(), 'clone', repos, request.pathname2url(target_path)]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = proc.communicate()

    if proc.returncode != 0:
        raise GoogkitError('Git clone failed: ' + result[1].decode())

    logging.debug(result[0].decode())
