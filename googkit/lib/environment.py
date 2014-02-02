class Environment(object):
    """Environment class that has runtime information.
    """

    def __init__(self, cwd, argument, tree):
        """Creates an environment by the cwd path, the Argument instance and the command tree.
        """
        self.cwd = cwd
        self.argument = argument
        self.tree = tree
