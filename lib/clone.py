import os


def run(repos, target_path):
    if os.path.exists(target_path):
        cwd = os.getcwd()
        os.chdir(target_path)
        os.system('git pull')
        os.chdir(cwd)
    else:
        os.system('git clone %s %s' % (repos, target_path))
