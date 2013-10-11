import os
import re
from cmds.command import Command
from lib.error import GoogkitError


class UpdateDepsCommand(Command):
    def __init__(self, env):
        super(UpdateDepsCommand, self).__init__(env)


    @classmethod
    def needs_config(cls):
        return True


    @classmethod
    def line_indent(cls, line):
        indent = ''
        m = re.search(r'^(\s*)', line)
        if len(m.groups()) >= 1:
            indent = m.group(1)

        return indent


    def update_deps(self):
        config = self.env.config
        js_dev_dir = config.js_dev_dir()
        deps_js = config.deps_js()

        base_js_dir = os.path.dirname(config.base_js())
        js_dev_dir_rel = os.path.relpath(js_dev_dir, base_js_dir)

        os.system('python %s --root_with_prefix="%s %s" --output_file="%s"' % (config.depswriter(), js_dev_dir, js_dev_dir_rel, deps_js))


    def update_tests(self, line, tests):
        joined = ','.join([('\'%s\'' % test_file) for test_file in tests])
        return 'var testFiles = [%s];' % joined


    def update_testrunner(self):
        config = self.env.config
        js_dev_dir = config.js_dev_dir()
        testrunner = config.testrunner()

        if not os.path.exists(testrunner):
            return

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

        lines = []

        for line in open(testrunner):
            marker = '/*@test_files@*/'
            if line.find(marker) >= 0:
                line = UpdateDepsCommand.line_indent(line) + self.update_tests(line, tests) + marker + '\n'

            lines.append(line)

        with open(testrunner, 'w') as f:
            for line in lines:
                f.write(line)


    def run_internal(self):
        print('Updating dependency information...')
        self.update_deps()
        self.update_testrunner()
