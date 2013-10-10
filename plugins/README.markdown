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


__init__.py
-----------
`__init__.py` is empty, but required to make Python treat the directory
as containing a package.


command.py
----------
`command.py` is your command.
Import `commands.command.Command` and extend `Command` class:

```python
from commands.command import Command


class PingCommand(Command):
    def run_internal(self):
        # TODO: Write your code here
        print('pong')
```

And add `register` function to register the command tree of Googkit:

```python
def register(tree):
    tree.register(['ping'], [PingCommand])
```
