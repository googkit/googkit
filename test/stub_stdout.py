# How to Use
# ==========
#
# * Silencing sys.stdout
#
#   from googkit.compat.unittest import mock
#   with patch('sys.stdout', new_callable = StubStdout):
#       print('this message will be not displayed')
#
#
# * Mocking sys.stdout
#
#   from googkit.compat.unittest import mock
#   MockStdout = mock.Mock(spec = StubStdout)
#   with patch('sys.stdout', new_callable = MockStdout) as mock_stdout:
#       print('this message will be not displayed')
#       print('you can assert stdout')
#
#   mock_stdout.write.assert_called_with('you can assert stdout')


# Check whether bytes aliased to str.
# In Python 2.x, bytes aliaased to str, but Python 3.x is defferent.
# Hooking stdout by io.StringIO will be failed on Python 3.x for the reason.
#
# http://docs.python.org/3.3/howto/pyporting.html#bytes-literals
try:
    b'a' + u'b'

    # Python 2.x
    from io import BytesIO
    StubStdout = BytesIO
except TypeError:

    # Python 3.x
    from io import StringIO
    StubStdout = StringIO
