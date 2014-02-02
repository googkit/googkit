class OptionBuilder(object):
    """A class for the option builders for shell commands.

    Usage::
        >>> args = OptionBuilder()
        >>> args.add('--arg1')
        >>> args.add('--arg2', 'value')
        >>> args.add('--arg3', 'subkey=value')
        >>> str(args)
        '--arg1 --arg2=value --arg3=subkey=value'
    """

    class OptionEntry(object):
        """A class for option entries.
        This entry is a container of a key and the value.
        """

        def __init__(self, key, value=None):
            """Creates an option entry with the specified key and the optional value.
            This option entry can be a key-only entry by giving None as the value.
            """
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
        self._args = []

    def __eq__(self, other):
        return self._args == other._args

    def __str__(self):
        return ' '.join([str(entry) for entry in self._args])

    def __iter__(self):
        return iter(self._args)

    def add(self, key, value=None):
        """Adds a key-value style argument to the argument list.

        Usage::
            >>> args = OptionBuilder()
            >>> args.add('--key1')
            >>> args.add('--key2', 'value1')
            >>> args.add('--key3', 'subkey=value')
        """
        entry = OptionBuilder.OptionEntry(key, value)
        self._args.append(entry)
