import logging
import os
import re
import subprocess
from googkit.commands.command import Command
from googkit.lib.error import GoogkitError


class UpdateDepsCommand(Command):
    @classmethod
    def needs_project_config(cls):
        return True

    @classmethod
    def line_indent(cls, line):
        indent = ''
        m = re.search(r'^(\s*)', line)
        if len(m.groups()) >= 1:
            indent = m.group(1)

        return indent

    def update_deps(self):
        config = self.config
        js_dev_dir = config.js_dev_dir()
        deps_js = config.deps_js()

        base_js_dir = os.path.dirname(config.base_js())
        js_dev_dir_rel = os.path.relpath(js_dev_dir, base_js_dir)

        args = [
            'python',
            config.depswriter(),
            '--root_with_prefix="{js_dev} {js_dev_rel}"'.format(js_dev=js_dev_dir, js_dev_rel=js_dev_dir_rel),
            '--output_file="{deps_js}"'.format(js_dev=js_dev_dir, js_dev_rel=js_dev_dir_rel, deps_js=deps_js)
        ]

        logging.info('Updating dependency information...')

        # depswriter.py doesn't work with arguments including white-space.
        # For example,
        #   it works:
        #
        #     $ python depswriter.py --root_with_prefix="path path"
        #
        #   but it doesn't work:
        #
        #     $ python depswriter.py "--root_with_prefix=\"path path\""
        proc = subprocess.Popen(' '.join(args), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = proc.communicate()

        if proc.returncode != 0:
            raise GoogkitError('Updating dependencies failed: ' + result[1])
        else:
            logging.debug(result[1])

        logging.info('Done.')

    def update_tests(self, line, tests):
        joined = ','.join(['\'' + test_file + '\'' for test_file in tests])
        return 'var testFiles = [{test_files}];'.format(test_files=joined)

    def update_testrunner(self):
        config = self.config
        js_dev_dir = config.js_dev_dir()
        testrunner = config.testrunner()

        if not os.path.exists(testrunner):
            return

        logging.info('Updating dependencies for unit-testing...')

        testrunner_dir = os.path.dirname(testrunner)
        test_file_pattern = config.test_file_pattern()
        tests = []

        for dirpath, dirnames, filenames in os.walk(js_dev_dir):
            for filename in filenames:
                if re.search(test_file_pattern, filename) is None:
                    continue

                path = os.path.join(dirpath, filename)
                relpath = os.path.relpath(path, testrunner_dir)

                tests.append(relpath)
                logging.debug('Test case found on ' + path)

        lines = []

        for line in open(testrunner):
            marker = '/*@test_files@*/'
            if line.find(marker) >= 0:
                indent = UpdateDepsCommand.line_indent(line)
                line = indent + self.update_tests(line, tests) + marker + '\n'

            lines.append(line)

        with open(testrunner, 'w') as f:
            for line in lines:
                f.write(line)

        logging.info('Done.')

    def run_internal(self):
        self.update_deps()
        self.update_testrunner()
