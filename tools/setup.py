#!/usr/bin/env python


import os
import os.path
import shutil


def command_exists(command):
    # TODO: Improve strictness
    with os.popen(command + ' --help') as p:
        return p.read() != ''


def setup_closure_library():
    if command_exists('svn'):
        os.system('svn checkout http://closure-library.googlecode.com/svn/trunk closure/library')
    elif command_exists('git'):
        os.system('git clone https://github.com/jarib/google-closure-library closure/library')
    else:
        print '[Error] Git or Subversion not found.'
        print 'Please install one of them to download Closure Library.'
        sys.exit()


def setup_closure_compiler():
    os.makedirs('tmp')

    os.system('python tools/sub/download.py http://closure-compiler.googlecode.com/files/compiler-latest.zip tmp/compiler.zip')

    os.makedirs('closure/compiler')
    os.system('python tools/sub/unzip.py tmp/compiler.zip closure/compiler')

    shutil.rmtree('tmp')


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(basedir)

    print 'Downloading Closure Library...'
    setup_closure_library()

    print 'Downloading Closure Compiler...'
    setup_closure_compiler()
