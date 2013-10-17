import unittest

from compat.unittest import mock
from test.stub_stdout import StubStdout
from test.stub_environment import StubEnvironment

from googkit.commands.command import Command
from googkit.lib.argument_parser import ArgumentParser
from googkit.lib.error import GoogkitError


class TestCommand(unittest.TestCase):
    def test_run(self):
        class DummyCommand(Command):
            pass

        env = StubEnvironment()
        env.arg_parser = ArgumentParser()
        cmd = DummyCommand(env)
        cmd._setup = mock.MagicMock()
        cmd.run_internal = mock.MagicMock()
        cmd.complete = mock.MagicMock()

        with mock.patch('sys.stdout', new_callable=StubStdout):
            cmd.run()

        cmd._setup.assert_called_once()
        cmd.run_internal.assert_called_once()
        cmd.complete.assert_called_once()

    def test_validate_options(self):
        class DummyCommand(Command):
            @classmethod
            def supported_options(cls):
                return set(['--foo', '--bar'])

        env = StubEnvironment()
        env.arg_parser = ArgumentParser()

        # No options should not raise any error
        env.arg_parser.parse(['googkit.py'])
        cmd = DummyCommand(env)
        cmd._validate_options()

        # Supported option should not raise any error
        env.arg_parser.parse(['googkit.py', '--foo'])
        cmd = DummyCommand(env)
        cmd._validate_options()

        # Unsupported option
        env.arg_parser.parse(['googkit.py', '--foo', '--blue-rose'])
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

        mock_usr_cfg.assert_called_once()
        mock_def_cfg.assert_called_once()
        mock_proj_cfg.assert_called_once()
        MockConfig.return_value.load.assert_called_once()


if __name__ == '__main__':
    unittest.main()
