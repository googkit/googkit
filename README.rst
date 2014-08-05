Googkit
=======


.. image:: https://pypip.in/version/googkit/badge.svg
   :target: https://crate.io/packages/googkit

.. image:: https://travis-ci.org/googkit/googkit.svg?branch=master
    :target: https://travis-ci.org/googkit/googkit




Overview
--------
Googkit is a tool that boosts development cycle of your web app with Google
Closure Library. You can setup your project only two steps so start developing
quickly. You can also do such a complicated compiling... by one command!


Requirements
~~~~~~~~~~~~
Googkit requires Following commands.
Install them if not installed yet.

:Git:    downloads Closure Library
:Python: executes Closure Tools




Install Googkit
---------------
First, you need to install Googkit.


Linux or OS X
~~~~~~~~~~~~~

1. Download and extract `the latest version of Googkit <https://github.com/googkit/googkit/releases>`_


2. Put it into a preferred place::

     $ mv googkit /opt


3. Add environment variables::

     export GOOGKIT_HOME=/opt/googkit
     export PATH=$PATH:$GOOGKIT_HOME/bin


Windows
~~~~~~~

1. Download and extract `the latest version of Googkit <https://github.com/googkit/googkit/releases>`_


2. Put it into a preferred place::

     $ move googkit C:\


3. Add environment variables

   +------------------+--------------------------------+
   | Variable         | Value                          |
   +==================+================================+
   | ``GOOGKIT_HOME`` | ``C:\googkit``                 |
   +------------------+--------------------------------+
   | ``PATH``         | Append ``;%GOOGKIT_HOME%\bin`` |
   +------------------+--------------------------------+




Getting Started
---------------
1. Create a project directory and initialize::

     $ mkdir my_project
     $ cd my_project
     $ googkit init


2. Download Closure Tools::

     $ googkit setup


3. Develop your web app in ``development/``

   Modify existing scripts, or add your awesome scripts
   to ``development/js_dev``.

   After adding/removing scripts, you need to update dependency information::

     $ googkit ready


4. Build your project

   Building the project including JavaScript files compilation improves
   performance and makes them unreadable::

     $ googkit build

   If it succeed, output files will be stored in ``production/``.




Project Structure
-----------------
:googkit.cfg:  config file of the project
:closure/:     stores Closure Tools
:development/: for development
:debug/:       for debug (it will be created if debug is enabled)
:production/:  for production




Running Unit Tests
------------------
You can run `jsunit-style <http://people.apache.org/~dennisbyrne/infoq/js_tdd.2.htm>`_
unit tests.


1. Create a HTML file for testing

   Copy `example_test.html <https://github.com/googkit/googkit/blob/master/template/development/js_dev/example_test.html>`_
   into the same directory as the target, then rename it to
   ``{target_name}_test.html``.

   If you don't like the default name ``{target_name}_test.html``, you can
   change it by ``test_file_pattern`` in ``googkit.cfg``.


2. Write unit tests


3. Apply config changes and update dependency information::

     $ googkit ready


4. Run unit tests

   Open the test html file in your browser.

   If you want to run all tests, open ``development/all_tests.html``
   in your browser with **http scheme** (doesn't work with file scheme).




Tips
----


Renaming a Compiled Script
~~~~~~~~~~~~~~~~~~~~~~~~~~
Edit ``compiled_js`` in ``googkit.cfg``.
After editing, apply it with a following command::

  $ googkit ready


Preventing Some Scripts from Compiling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Place them outside ``development/js_dev``.
Scripts that are in it will be compiled and removed in production.


Debugging a Compiled Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Build with ``--debug`` option::

  $ googkit build --debug

Then you can use debugging features in ``debug/``.


Using Source Map
~~~~~~~~~~~~~~~~
Googkit generates a source map file ``script.min.js.map`` within ``debug/``,
so you can use `Source Map V3 <https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit?pli=1>`_
if your browser supports it.

For reason of obfuscation, source map file will **NOT** be stored
in ``production/``.




Misc
----


The Googkit team
~~~~~~~~~~~~~~~~
- cocopon (cocopon@me.com)
- OrgaChem (orga.chem.job@gmail.com)


License
~~~~~~~
Googkit are licensed under MIT License.
See ``LICENSE.txt`` for more information.
