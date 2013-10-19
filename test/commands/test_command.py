import unittest

from test.stub_environment import StubEnvironment
from test.stub_stdout import StubStdout

from googkit.commands.command import Command
from googkit.compat.unittest import mock
from googkit.lib.argument import Argument
from googkit.lib.argument import ArgumentParser
from googkit.lib.error import GoogkitError


class TestCommand(unittest.TestCase):
    def test_run(self):
        class DummyCommand(Command):
            pass

        env = StubEnvironment()
        env.argument = Argument()
        cmd = DummyCommand(env)
        cmd._setup = mock.MagicMock()
        cmd.run_internal = mock.MagicMock()

        with mock.patch('sys.stdout', new_callable=StubStdout):
            cmd.run()

        self.assertTrue(cmd._setup.called)
        self.assertTrue(cmd.run_internal.called)

    def test_validate_options(self):
        class DummyCommand(Command):
            @classmethod
            def supported_options(cls):
                return set(['--foo', '--bar'])

        env = StubEnvironment()

        # No options should not raise any error
        env.argument = ArgumentParser.parse(['googkit.py'])
        cmd = DummyCommand(env)
        cmd._validate_options()

        # Supported option should not raise any error
        env.argument = ArgumentParser.parse(['googkit.py', '--foo'])
        cmd = DummyCommand(env)
        cmd._validate_options()

        # Unsupported option
        env.argument = ArgumentParser.parse(['googkit.py', '--foo', '--blue-rose'])
        cmd = DummyCommand(env)
        with self.assertRaises(GoogkitError):
            cmd._validate_options()

    def test_setup(self):
        class DummyCommand(Command):
            def _load_config_if_needed(self):
                pass

        env = StubEnvironment()
        env.cwd = '/cwd'

        cmd = DummyCommand(env)
        cmd._load_config_if_needed = mock.MagicMock()

        with mock.patch('os.chdir') as mock_chdir:
            cmd._setup()

            mock_chdir.assert_called_once_with('/cwd')

    def test_load_config(self):
        class ConcreteCommandNeedsConfig(Command):
            @classmethod
            def needs_config(cls):
                return True

        with mock.patch('googkit.lib.path.user_config') as mock_usr_cfg, \
                mock.patch('googkit.lib.path.default_config') as mock_def_cfg, \
                mock.patch('googkit.lib.path.project_config') as mock_proj_cfg, \
                mock.patch('googkit.commands.command.Config') as MockConfig:
            mock_usr_cfg.return_value = '/dummy/.googkit'
            mock_def_cfg.return_value = '/dummy/default.cfg'
            mock_proj_cfg.return_value = '/dummy/googkit.cfg'
            MockConfig.load.return_value = mock.MagicMock()

            env = StubEnvironment()
            cmd = ConcreteCommandNeedsConfig(env)

            result = cmd._load_config()

            self.assertIsNotNone(result)

        self.assertTrue(mock_usr_cfg.called)
        self.assertTrue(mock_def_cfg.called)
        self.assertTrue(mock_proj_cfg.called)
        self.assertTrue(MockConfig.return_value.load.called)


if __name__ == '__main__':
    unittest.main()
