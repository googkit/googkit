class ArgumentBuilder(object):
    """A class for the argument Builder.

    Usage::
        >>> args = ArgumentBuilder()
        >>> args.add('--arg1', 'ARG1')
        >>> args.add('--arg2', 'ARG2')
        >>> args.add('--arg3')
        >>> sorted(str(arg) for arg in args)
        ['--arg1=ARG1', '--arg2=ARG2', '--arg3']
    """
    class ArgumentEntry(object):
        def __init__(self, key, value=None):
            self.key = key
            self.value = value

        def __str__(self):
            if self.value is None:
                return self.key
            else:
                return self.key + '=' + self.value

        def __eq__(self, other):
            return self.key == other.key and self.value == other.value

        def __hash__(self):
            return hash(str(self))

    def __init__(self):
        self._args = set()

    def __eq__(self, other):
        return self._args == other._args

    def __str__(self):
        return ' '.join([str(entry) for entry in self._args])

    def __iter__(self):
        return iter(self._args)

    def add(self, key, value=None):
        entry = ArgumentBuilder.ArgumentEntry(key, value)
        self._args.add(entry)
