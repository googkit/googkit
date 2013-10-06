from lib.error import GoogkitError


class Command(object):
    def __init__(self, env):
        self.env = env


    @classmethod
    def needs_config(cls):
        return False


    @classmethod
    def needs_global_config(cls):
        return False


    def run(self):
        if  self.__class__.needs_config() and self.env.config is None:
            raise GoogkitError('No config file found.')

        if  self.__class__.needs_global_config() and self.env.global_config is None:
            raise GoogkitError('No global config file found.')

        self.run_internal()
        self.complete()


    def run_internal(self):
        # Override the method to change the behavior
        pass 


    def complete(self):
        print('Completed.')
