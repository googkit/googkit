import os


def run(repos, target_path):
    # TODO: If target directory already exists, update repository
    os.system('git clone %s %s' % (repos, target_path))
