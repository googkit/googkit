import os


def run(repos, target_path):
    if os.path.exists(target_path):
        cwd = os.getcwd()
        os.chdir(target_path)
        os.system('git pull')
        os.chdir(cwd)
    else:
        cmd = 'git clone {repos} {tgt}'.format(repos=repos, tgt=target_path)
        os.system(cmd)
