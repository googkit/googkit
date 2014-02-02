import re

def line_indent(line):
    """Returns an indent at head of the specified line.

    Usage::
        >>> line_indent('    I have 4 spaces.')
        '    '
    """
    indent = ''
    m = re.search(r'^(\s*)', line)
    if len(m.groups()) >= 1:
        indent = m.group(1)

    return indent
