Localizing Googkit
==================
Googkit supports i18n.
You can localize messages in your language with
`gettext <https://www.gnu.org/software/gettext/>`_.


Requirements
------------
- xgettext
- msgfmt


Steps
-----

1. Make directory for i18n resource::

     $ cd $GOOGKIT_HOME
     $ cd googkit_data/locale
     $ mkdir -p ja/LC_MESSAGES
     (replace ``ja`` with your language)


2. Generate PO file::

     $ cd $GOOGKIT_HOME
     $ xgettext **/*.py -o googkit_data/locale/ja/LC_MESSAGES/googkit.po


3. Edit PO file and translate message resources


4. Convert PO file into MO file::

     $ cd $GOOGKIT_HOME
     $ cd googkit_data/locale/ja/LC_MESSAGES
     $ msgfmt googkit.po -o googkit.mo
