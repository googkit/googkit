How to Create Your Own Plugin
=============================


Directory Structure
-------------------
For example, if you want to create ``ping`` command, directory structure
will be as follows::

  googkit/
  |-- googkit/
  |   `-- plugins/
  |       `-- ping/
  |           |-- __init__.py
  :           `-- command.py


__init__.py
-----------
``__init__.py`` is empty, but required to make Python treat the directory
as containing a package.


command.py
----------
``command.py`` is your command.
Import ``Command`` class from  ``googkit.commands.command`` and extend it::

  from googkit.commands.command import Command
  
  
  class PingCommand(Command):
      def run_internal(self):
          # TODO: Write your code here
          print('pong')

And append ``register`` function to register ``ping`` command on
the command tree of Googkit::

  def register(tree):
      tree.register(['ping'], [PingCommand])
