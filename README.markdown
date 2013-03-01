Closure Library Starter Kit
===========================


Overview
--------
Closure Library Starter Kit is a starter kit for Closure Library newbies
(including me!).
You can easily setup, develop, and compile using convenient tools.


### System Requirement
Following programs are required to use this starter kit.
Install them if not installed yet.

- Git or Subversion ... Downloads Closure Library
- Python .............. Executes Closure Tools


### Directory Structure
- closure/ ....... Stores Closure Tools
- development/ ... For development
- production/ .... For production
- tools/ ......... Contains convenient tools


Getting Started
---------------
1. Setup Closure Tools

    Enter following commands in the terminal:

        (in `closure-starter-kit` directory)
        $ python tools/setup.py

2. Develop Your Web App in `development/`

    Modify existing scripts, or add awesome scripts to `development/js_dev`.

    After adding/removing scripts, you need to update dependency information:
 
        $ python tools/update_deps.py

3. Compile Scripts

    Compiling scripts improves performance and makes them unreadable.
    To compile your scripts, enter following command:

        $ python tools/compile.py

    If it succeed, output files will be stored in `production/`.


Tips
----
### Changing Namespace of Main Class
If you want to change the default namespace of Main class (com.mycompany.Main),
replace all namespaces in following files:

- development/index.html
- development/js_dev/main.js
- tools/compile.py

After changing, don't forget to update dependency information.

    $ python tools/update_deps.py


### Rename a Compiled Script
Edit `COMPILED_JS` in `tools/compile.py`.


### Preventing Some Scripts from Compiling
Place them outside `development/js_dev`.
Scripts that are in it will be compiled and removed in production.


Misc
----
### Author
cocopon (cocopon@me.com)


### License
MIT License. See `LICENSE.txt` for more information.
