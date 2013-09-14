goog-starter-kit
================


Overview
--------
goog-starter-kit is a starter kit for Google Closure Library newbies
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
- debug/ ......... For debug (it exists when `is_debug_enabled` in `tools/tools.cfg` is `yes`)
- production/ .... For production
- tools/ ......... Contains convenient tools


Getting Started
---------------
1. Setup Closure Tools

    Enter following commands in the terminal:

        (in `goog-starter-kit` directory)
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
If you want to change the default namespace of Main class (`foo.Main`),
change `main_namespace` in `tools/tools.cfg`.

After changing, don't forget to apply changes and update dependency information.

    $ python tools/apply_config.py
    $ python tools/update_deps.py


### Rename a Compiled Script
Edit `compiled_js` in `tools/tools.cfg`.


### Preventing Some Scripts from Compiling
Place them outside `development/js_dev`.
Scripts that are in it will be compiled and removed in production.


### Debug the Compiled Source
If you want to debug compiled script, change `is_debug_enabled` to `yes` in `tools/tools.cfg`.
If debug is enabled, you can use source map and debugging features by Closure Library in `debug/`, but it makes compilation slow.


#### Using Source Map
This kit support compilation with a source map (the source map file will be stored in `debug/` as `script.min.js.map`). You can use [Source Map V3](https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit?pli=1), if your browser was support it.

Additionaly, source map will be **NOT** stored in `production/` for obfuscation.


Misc
----
### Author
cocopon (cocopon@me.com)

### Contributors
OrgaChem (orga.chem.job@gmail.com)

### License
These tools are licensed under MIT License.
See `LICENSE.txt` for more information.
