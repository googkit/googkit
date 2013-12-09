Localizing Googkit
==================
Googkit supports i18n.
You can localize messages in your language with `gettext <http://TODO>`.


Requirements
------------
- xgettext
- msgfmt


Steps
-----

1. Make locale directory::

     $ cd $GOOGKIT_HOME/googkit_data/locale
     $ mkdir -p ja/LC_MESSAGES


2. Generate PO file::

     $ cd $GOOGKIT_HOME
     $ xgettext **/*.py -o googkit_data/locale/ja/LC_MESSAGES/googkit.po


3. Edit PO file and translate message resources


4. Convert PO file into MO file::

     $ cd googkit_data/locale/ja/LC_MESSAGES/
     $ msgfmt googkit.po
