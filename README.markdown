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

- Git ...... Downloads Closure Library
- Python ... Executes Closure Tools


### Directory Structure
- closure/ ....... Stores Closure Tools
- development/ ... For development
- debug/ ......... For debug (it will be created when `is_debug_enabled` is `yes` in `tools/tools.cfg`)
- production/ .... For production
- tools/ ......... Contains convenient tools




Getting Started
---------------
1. Setup Closure Tools

    Enter following commands in the terminal:

        (in `goog-starter-kit` directory)
        $ python tools/tool.py setup


2. Develop Your Web App in `development/`

    Modify existing scripts, or add awesome scripts to `development/js_dev`.

    After adding/removing scripts, you need to update dependency information:

        $ python tools/tool.py update-deps


3. Compile Scripts

    Compiling scripts improves performance and makes them unreadable.
    To compile your scripts, enter following command:

        $ python tools/tool.py compile

    If it succeed, output files will be stored in `production/`.




Running Unit Tests
------------------
You can run [jsunit-style](http://people.apache.org/~dennisbyrne/infoq/js_tdd.2.htm) unit tests.


1. Create a HTML File for Testing

    Copy [example_test.html](https://github.com/cocopon/goog-starter-kit/blob/master/development/js_dev/example_test.html) into the same directory as the target, then rename it to `{target_name}_test.html`.

    If you don't like the default name `{target_name}_test.html`, you can change it by `test_file_pattern` in `tools/tools.cfg`.


2. Apply Config Changes

    Enter following commands in the terminal:

        (in `goog-starter-kit` directory)
        $ python tools/tool.py apply-config


3. Write Unit Tests


4. Update Dependency Information

    Enter a following command in the terminal:

        $ python tools/tool.py update-deps


5. Run Unit Tests

    Open the test html file in your browser.

    If you want to run all tests, open `development/all_tests.html` in your browser with **http scheme** (doesn't work with file scheme).




Tips
----
### Changing Namespace of Main Class
If you want to change the default namespace of Main class (`foo.Main`),
change `main_namespace` in `tools/tools.cfg`.

After changing, don't forget to apply changes and update dependency information.

    $ python tools/tool.py apply-config
    $ python tools/tool.py update-deps


### Renaming a Compiled Script
Edit `compiled_js` in `tools/tools.cfg`.


### Preventing Some Scripts from Compiling
Place them outside `development/js_dev`.
Scripts that are in it will be compiled and removed in production.


### Debugging a Compiled Source
If you want to debug a compiled script, change `is_debug_enabled` to `yes` in `tools/tools.cfg`.
Then you can use a source map and debugging features by Closure Library in `debug/`.
This option makes compilation slow.


#### Using Source Map
This kit generates a source map file `script.min.js.map` within `debug/`, so you can use [Source Map V3](https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit?pli=1) if your browser supports it.

For reason of obfuscation, source map file will **NOT** be stored in `production/`.




Misc
----
### Author
cocopon (cocopon@me.com)


### Contributors
OrgaChem (orga.chem.job@gmail.com)


### License
These tools are licensed under MIT License.
See `LICENSE.txt` for more information.
