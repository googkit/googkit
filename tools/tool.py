#!/usr/bin/env python


import os
import os.path
import sys
import toolsconfig
from setup import SetupCommand


CONFIG = os.path.join('tools', 'tools.cfg')


def print_help():
    print 'TODO: Help'


if len(sys.argv) != 2:
    print_help()
    sys.exit()

subcommand = sys.argv[1]

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(basedir)
config = toolsconfig.ToolsConfig()
config.load(CONFIG)

if subcommand == 'setup':
    SetupCommand(config).run()
