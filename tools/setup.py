#!/usr/bin/env python


CONFIG = 'config.cfg'
LIBRARY_SVN_REPOS = 'http://closure-library.googlecode.com/svn/trunk'
LIBRARY_GIT_REPOS = 'https://github.com/jarib/google-closure-library'
COMPILER_SVN_REPOS = 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'


import os
import os.path
import shutil
import cskconfig


def command_exists(command):
    # TODO: Improve strictness
    with os.popen(command + ' --help') as p:
        return p.read() != ''


def setup_closure_library(config):
    if command_exists('svn'):
        os.system('svn checkout %s %s' % (LIBRARY_SVN_REPOS, config.library_local_root()))
    elif command_exists('git'):
        os.system('git clone %s %s' % (LIBRARY_GIT_REPOS, config.library_local_root()))
    else:
        print '[Error] Git or Subversion not found.'
        print 'Please install one of them to download Closure Library.'
        sys.exit()


def setup_closure_compiler(config):
    os.makedirs('tmp')

    subtool_download = os.path.join('tools', 'sub', 'download.py')
    compiler_zip = os.path.join('tmp', 'compiler.zip')
    os.system('python %s %s %s' % (subtool_download, COMPILER_SVN_REPOS, compiler_zip))

    compiler_root = config.compiler_root()
    os.makedirs(compiler_root)

    subtool_unzip = os.path.join('tools', 'sub', 'unzip.py')
    os.system('python %s %s %s' % (subtool_unzip, compiler_zip, compiler_root))

    shutil.rmtree('tmp')


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    config = cskconfig.CskConfig()
    config.load(CONFIG)

    print 'Downloading Closure Library...'
    setup_closure_library(config)

    print 'Downloading Closure Compiler...'
    setup_closure_compiler(config)
