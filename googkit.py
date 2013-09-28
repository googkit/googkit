import os
import sys
from commands.apply_config import ApplyConfigCommand
from commands.compile import CompileCommand
from commands.init import InitCommand
from commands.setup import SetupCommand
from commands.update_deps import UpdateDepsCommand
from lib.config import Config
from lib.error import GoogkitError


CONFIG = 'googkit.cfg'
COMMANDS_DICT = {
        'apply-config': [ApplyConfigCommand, UpdateDepsCommand],
        'compile': [CompileCommand],
        'init': [InitCommand],
        'setup': [SetupCommand, UpdateDepsCommand],
        'update-deps': [UpdateDepsCommand]}


def print_help():
    print('Usage: googkit command')
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

config = None
try:
    config = Config()
    config.load(CONFIG)
except IOError:
    config = None

try:
    for klass in subcommand_classes:
        subcommand = klass(config)
        subcommand.run()
except GoogkitError, e:
    sys.exit('[ERROR] ' + str(e))
