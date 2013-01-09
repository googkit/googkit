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

- bash ...... Executes tools
- curl ...... Downloads Closure Compiler
- git/svn ... Downloads Closure Library
- python .... Executes Closure Tools
- sed ....... Executes tools


### Directory Structure
- closure/ ... Stores Closure Tools
- debug/ ..... For development
- release/ ... For production
- tools/ ..... Contains convenient tools


Getting Started
---------------
1. Setup Closure Tools
Enter following commands in the terminal:

    (in `closure-starter-kit` directory)
    $ ./tools/setup.sh

2. Develop Your Web App in `debug/`
Modify existing scripts, or add awesome scripts to `debug/js_dev`.

After adding/removing scripts, you need to update dependency information:
 
    $ ./tools/update_deps.sh

3. Compile Scripts
Compiling scripts improves performance and makes them unreadable.
To compile your scripts, enter following command:

    $ ./tools/compile.sh

If it succeed, output files will be stored in `release/`.


Tips
----
### Changing Namespace of Main Class
If you want to change the default namespace of Main class (com.mycompany.Main),
replace all namespaces in following files:

- debug/index.html
- debug/js_dev/main.js
- tools/compile.sh

After changing, don't forget to update dependency information.

    $ ./tools/update_deps.sh


### Rename a Compiled Script
Edit `COMPILED_JS` in `tools/compile.sh`.


### Preventing Some Scripts from Compiling
Place them outside `debug/js_dev`.
Scripts that are in it will be compiled and removed in production.


Misc
----
### Author
cocopon (cocopon@me.com)

### License
MIT License. See `LICENSE.txt` for more information.
