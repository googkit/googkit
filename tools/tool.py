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
COMMANDS_DICT = {
        'apply-config': [ApplyConfigCommand, UpdateDepsCommand],
        'compile': [CompileCommand],
        'setup': [SetupCommand],
        'update-deps': [UpdateDepsCommand]}


def print_help():
    print('Usage: python tool.py command')
    print('')
    print('Available subcommands:')

    for name in sorted(COMMANDS_DICT.keys()):
        print('    ' + name)


if len(sys.argv) != 2:
    print_help()
    sys.exit()

subcommand_classes = COMMANDS_DICT.get(sys.argv[1])
if subcommand_classes is None:
    print_help()
    sys.exit()

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(basedir)
config = toolsconfig.ToolsConfig()
config.load(CONFIG)

for klass in subcommand_classes:
    subcommand = klass(config)
    subcommand.run()
