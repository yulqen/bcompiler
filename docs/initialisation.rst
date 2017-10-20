Initialise bcompiler
++++++++++++++++++++++

``bcompiler`` needs auxiliary files to run, including a ``datamap.csv`` and ``config.ini`` files. These files are stored in a directory called ``bcompiler`` in your ``Documents`` directory. Before running ``bcompiler``, this directory structure needs to be set up. The auxiliary files also need to be downloaded from a `git repository on Github <https://github.com/departmentfortransport/bcompiler_datamap_files>`_. ``bcompiler`` can do the necessary work to set this up.

* In the command window, type ``bcompiler-init``.

Changing settings for various things in ``bcompiler`` is done using
a :ref:`config` file.

Auxiliary files
~~~~~~~~~~~~~~~
``bcompiler`` requires three files to be present in the auxiliary directory,
created during ``bcompiler-init``:

- ``config.ini``
- ``datamap.csv``
- ``bicc_template.xlsm``

.. _config:

config.ini
-----------

This is a text file in ``Documents/bcompiler/source`` that allows allows the
user to set basic configuration options.

`INI <https://en.wikipedia.org/wiki/INI_file>`_ files are an informal standard for configuration files. The basic element contained in an INI file is the *key* or *property*. Every key has a *name* and *value*, delimted by an equals sign (=). The name appears to the left of the equals sign.

Keys may be grouped into sections (this is the case for ``bcompiler``). The
section name appears on a line by itself in square brackets ([ and  ]). All
keys declared after the section declaration are associated with that section.

Example:

.. code:: ini

    [QuarterData]
    CurrentQuarter = Q2 Jul - Oct 2017

The options available to set for ``bcompiler`` are:

+----------------------------+----------------------------------------------------------------------------------+
|Purpose                     |Description                                                                       |
+============================+==================================================================================+
|QuarterData                 |In ``Q2 Jul - Oct 2017``. Appears in appropriate field in template.               |
+----------------------------+----------------------------------------------------------------------------------+
|TemplateSheets              |The names of each relevant sheet in the template must be set here                 |
+----------------------------+----------------------------------------------------------------------------------+
|BlankTemplate               |Set the name of the template kept in the `Documents/bcompiler/source directory`   |
+----------------------------+----------------------------------------------------------------------------------+
|Datamap                     |Set the name of the datamap kept in the `Documents/bcompiler/source directory`    |
+----------------------------+----------------------------------------------------------------------------------+
|Master                      |Set the name of the master file kept in the `Documents/bcompiler/source directory`|
+----------------------------+----------------------------------------------------------------------------------+

Note that sensible values are set by default. The option you will most likely
need to change is ``Master`` as this is most often renamed by the user ourside
of ``bcompiler`` use.


datamap.csv
-----------

In order for ``bcompiler`` to retrieve data from cells in an Excel spreadsheet,
it requires a mapping between the master to the template. This is achieved in
a CSV file with the following headers:

- **cell_key**: The name of the value as it appears in Column A of the master
- **template_sheet**: The name of the sheet in the template
- **cell_reference**: The cell reference of the cell where data lives in the template
- **verification_list**: **LEGACY** Not currently implemented


bicc_template.xlsm
------------------

The Excel file that is populated by ``bcompiler`` and sent to project teams and
subsquently queried by ``bcompiler`` when populating the master spreadsheet.
Contains macros to handle cell verification so must be saved in ``.xlsm``
format.


Other options
~~~~~~~~~~~~~

- In a command window, run ``bcompiler --help`` to see other options. **Please
  note**: some of these are legacy options and will be changed or removed in
  future versions of ``bcompiler``.
