import logging
import os
import subprocess
from googkit.compat.urllib import request
from googkit.lib.error import GoogkitError
from googkit.lib.i18n import _


def run(repos, target_path):
    """Clone the specified repository to the target path.
    """
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
    popen_args = {
        'cwd': target_path,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
    }

    proc = subprocess.Popen(args, **popen_args)
    result = proc.communicate()

    if proc.returncode != 0:
        raise GoogkitError(_('Git pull failed: {message}').format(
            message=result[1].decode()))

    logging.debug(result[0].decode())


def _clone(repos, target_path):
    # git-clone on Windows expected unix-like path
    args = [_git_cmd(), 'clone', repos, request.pathname2url(target_path)]
    popen_args = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
    }

    proc = subprocess.Popen(args, **popen_args)
    result = proc.communicate()

    if proc.returncode != 0:
        raise GoogkitError(_('Git clone failed: {message}').format(
            message=result[1].decode()))

    logging.debug(result[0].decode())
