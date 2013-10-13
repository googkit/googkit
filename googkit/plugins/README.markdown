How to Create Your Own Plugin
=============================


Directory Structure
-------------------
If you want to create `ping` command, directory structure will be as follows:

```
- googkit/
|  + bin/
|  ...
|
|  - plugins/
|  |  - ping/
|  |  |  __init__.py
|  |  |  command.py
```


\_\_init\_\_.py
---------------
`__init__.py` is empty, but required to make Python treat the directory
as containing a package.


command.py
----------
`command.py` is your command.
Import `commands.command.Command` and extend `Command` class:

```python
from cmds.command import Command


class PingCommand(Command):
    def run_internal(self):
        # TODO: Write your code here
        print('pong')
```

And append `register` function to register `ping` command on the command tree
of Googkit:

```python
def register(tree):
    tree.register(['ping'], [PingCommand])
```
