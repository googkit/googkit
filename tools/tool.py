#!/usr/bin/env python


import os
import os.path
import sys
import toolsconfig
from commands.apply_config import ApplyConfigCommand
from commands.compile import CompileCommand
from commands.setup import SetupCommand
from commands.update_deps import UpdateDepsCommand


CONFIG = os.path.join('tools', 'tools.cfg')
COMMANDS = {
        'apply-config': ApplyConfigCommand,
        'compile': CompileCommand,
        'setup': SetupCommand,
        'update-deps': UpdateDepsCommand}


def print_help():
    print ('TODO: Help')


if len(sys.argv) != 2:
    print_help()
    sys.exit()

subcommand_class = COMMANDS.get(sys.argv[1])
if subcommand_class is None:
    print_help()
    sys.exit()

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(basedir)
config = toolsconfig.ToolsConfig()
config.load(CONFIG)

subcommand = subcommand_class(config)
subcommand.run()
