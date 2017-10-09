bcompiler
=========

.. contents::
    :depth: 2
    :backlinks: top
    :local:

Quick Start
-----------

* Ensure Python 3.6.2 or later is installed on your system.
* Ensure git is installed on your system.
* ``pip install bcompiler``
* ``bcompiler-init``
* ``bcompiler --help``


Introduction
-------------

``bcompiler`` is a tool to manage data involved in the BICC reporting process at the UK Department for Transport.

``bcompiler`` processes data held in Excel files, either compiling similar data
from many Excel files into a single master spreadsheet, or populating many
Excel files using the data from a master spreadsheet.

"Auxiliary" files are required to map data in each direction, and to templates.
These files are contained in a DfT reporitory on GitHub. ``bcompiler`` can be
used to obtain/update these files.


Installation (Windows)
----------------------

Install Python
+++++++++++++++++++++

1. To install Python, download installer file from
   http://www.python.org/ftp/python/3.6.2/python-3.6.2.exe. Choose to
   save it to a location on your harddrive, such as your Desktop or Downloads
   folder.
2. Run the installer. On the Install Python Setup screen, ensure "Add
   Python 3.6 to PATH" and "Install launcher for all users (recommended)" is checked. Click "Install Now".
3. Open a new command window (Start -> type "cmd" in Search box and hit enter).

Update pip (if required)
++++++++++++++++++++++++

* In command window, type ``python -m pip install -U pip``.


Install git
+++++++++++

1. Go to https://git-scm.com/download/win. The download will begin
   automatically. Save it to a location on your hardrive, such as your Desktop
   or Downloads folder.
2. Run the installer, accepting all default options. If you get a message
   saying that you cannot run the 64-bit installer, choose the 32-bit installer
   from the above page.

Install bcompiler
+++++++++++++++++

* If you do not already have ``bcompiler`` installed, in the command window, type ``pip install bcompiler``.
* If you have ``bcompiler`` installed, it is a good idea to update to the latest version. In the command window, type ``pip install -U bcompiler``.


Initialise bcompiler
++++++++++++++++++++++

``bcompiler`` needs auxiliary files to run, including a ``datamap.csv`` and ``config.ini`` files. These files are stored in a directory called ``bcompiler`` in your ``Documents`` directory. Before running ``bcompiler``, this directory structure needs to be set up. The auxiliary files also need to be downloaded from a `git repository on Github <https://github.com/departmentfortransport/bcompiler_datamap_files>_. ``bcompiler`` can do the necessary work to set this up.

* In the command window, type ``bcompiler-init``.

Setting options
---------------

Auxiliary files
+++++++++++++++

``bcompiler`` requires three files to be present in the auxiliary directory,
created during ``bcompiler-init``:

- ``config.ini``
- ``datamap.csv``
- ``bicc_template.xlsm``

config.ini
==============

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

+----------------------------+--------------------------------------------------------------------------------+
|Purpose                     |Description                                                                     |
+============================+================================================================================+
|QuarterData                 |In ``Q2 Jul - Oct 2017``. Appears in appropriate field in template.             |
+----------------------------+--------------------------------------------------------------------------------+
|TemplateSheets              |The names of each relevant sheet in the template must be set here               |
+----------------------------+--------------------------------------------------------------------------------+
|BlankTemplate               |Set the name of the template kept in the `Documents/bcompiler/source directory`   |
+----------------------------+--------------------------------------------------------------------------------+
|Datamap                     |Set the name of the datamap kept in the `Documents/bcompiler/source directory`    |
+----------------------------+--------------------------------------------------------------------------------+
|Master                      |Set the name of the master file kept in the `Documents/bcompiler/source directory`|
+----------------------------+--------------------------------------------------------------------------------+

Note that sensible values are set by default. The option you will most likely
need to change is ``Master`` as this is most often renamed by the user ourside
of ``bcompiler`` use.


datamap.csv
==============

In order for ``bcompiler`` to retrieve data from cells in an Excel spreadsheet,
it requires a mapping between the master to the template. This is achieved in
a CSV file with the following headers:

- **cell_key**: The name of the value as it appears in Column A of the master
- **template_sheet**: The name of the sheet in the template
- **cell_reference**: The cell reference of the cell where data lives in the template
- **verification_list**: **LEGACY** Not currently implemented


bicc_template.xlsm
====================

The Excel file that is populated by ``bcompiler`` and sent to project teams and
subsquently queried by ``bcompiler`` when populating the master spreadsheet.
Contains macros to handle cell verification so must be saved in ``.xlsm``
format.


Creating a master spreadsheet from populated templates
-------------------------------------------------------

- Ensure all populated returns are copied to the ``Documents/bcompiler/source/returns`` directory. Ensure no other files are present in this directory.
- In a command window, run ``bcompiler`` (no arguments are required).
- The resulting master file will be created in ``Documents/bcompiler/output`` directory.
- To compare values from a previous master, run ``bcompiler --compare <PATH-TO-MASTER-TO-COMPARE>``


Populating templates based on a master spreadsheet
--------------------------------------------------

- Ensure the master spreadsheet is in the ``Documents/bcompiler/source`` directory.
- Ensure the filename of the master spreadsheet is included in the ``[Master]`` section in ``config.ini``.
- In a command window, run ``bcompiler -a``.
- The resulting files will be created in ``Documents/bcompiler/output``.

Check integrity of populated template files
-------------------------------------------

The template used to collect data should not be changed by the user; allowing
the user to add rows or columns will cause a world of problems for
``bcompiler``. To ensure the integrity of the template, sheets in
``bicc_template.xlsm`` are locked to prevent rows being added or deleted.

However, ``bcompiler`` is able to check the validity of all returned templates
if required, by comparing the number of rows in each sheet with what it expects
from ``bicc_template.xlsm``.

- Ensure all populated returns are copied to
  ``Documents/bcompiler/source/returns``.
- In a command window, run ``bcompiler -r``

This will print the count of rows in each sheet in each template file. Any row
count that differs from the equivalent sheet in ``bicc_template.xlsm`` will be
marked with a `*`.

- To output this data to the ``Documents/bcompiler/output`` directory, run
  ``bcompiler -r --csv``.
- To only show differences between the file and ``bicc_template.xlsm``, run
  ``bcompiler -r --quiet``.

Other options
--------------

- In a command window, run ``bcompiler --help`` to see other options. **Please
  note**: some of these are legacy options and will be changed or removed in
  future versions of ``bcompiler``.

Known bugs and issues
---------------------
* See above
