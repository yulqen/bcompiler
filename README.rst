BCompiler
=========

Introduction
-------------

``bcompiler`` is a tool manage data involved in the BICC reporting process at DfT. It is designed to provide a basic data processing function and making storing, cleaning and analysing the data historically contained in MS Excel files easier to manage.

It is currently a command line-only tool but future versions may involve a GUI or web interface.

``bcompiler`` performs to types of jobs: **populating** and **compiling**.

Populating
^^^^^^^^^^^

**Populating** describes pulling data from a *master database* or spreadsheet into *multiple Excel files* for distribution to others.

Compiling
^^^^^^^^^^

**Compiling** describes collating data from *multiple separate Excel files* into a *master database* or spreadsheet for storing the data and using as the basis for subsequent analysis.

The following table provides a summary of the main tasks:

+------------------------+-----------------------+
| Populating             | Compiling             |
+========================+=======================+
| Master to BICC Returns | BICC Returns to Master|
+------------------------+-----------------------+
| Master to GMPP Return  |                       |
+------------------------+-----------------------+

Working Directory and Files
----------------------------

``bcompiler`` works with external files, therefore it a directory in which to hold these files, as well as directories for output.

By default, this main directory intended to hold these external files is at:

``~/Documents/bcompiler`` (or equivalent on Windows)

how it is **not** created automatically unless the user directs this. Therefore the first action should be to create this directory using:

``bcompiler --create-wd``

If the directory currently exists, this will be reported to you. As you may have existing files in the working diretory which are key to the job at hand (such as a ``datamap`` file or a ``master.csv`` file), BCompiler will leave the directory untouched. However, if you wish to delete old working files and start from scratch, you may issue:

``bcompiler --force-create-wd`` which will remove the old directory and create a clean one.

Source files
^^^^^^^^^^^^^

Once you have created the requisite folder structure, you must then ensure the correct source files have been deposited in the ``bcompiler/source/``.

The following files are required for the purposes of populating (*Master to BICC* or *Master to GMPP*):

**master.csv**
    a CSV version of the master spreadsheet

**bicc_template.xlsx**
    a blank BICC Return template in Excel

**datamap**
    a comma-separated datamap file linking cell


master.csv
+++++++++++

This file can be created manually or could be the output from a *BICC Returns to Master* compilaton process. The traditonal structure for this file was a reverse-csv format, such as:

::

    Project/Programme Name,A14 Road Reconstruction,A303 Layby Maintenance,..
    Classification,DfT-102,DfT-102,..
    SRO Name,Jim Smith,Carol Heggarty,...
    SRO Training,SRO Master Practictioner,SRO Novice,...
    ...

bicc_template.xls
++++++++++++++++++

This file needs to be a blank xlsx form. It needs to be xlsx because it needs to have multiple tabs and formulas, etc embedded in it. It will be populated by the *Master to BICC* process, whose aim is to provide a partially populated form for each project team in the BICC Portfolio. This will normally be the result of the converse process in the system, namely the *BICC Returns to Master* process, where the data for that project for the previous quarter was compiled into the master database.

By doing this, the project team receive a 'blank' form that is familiar to them, in that it holds most of the data they submitted the previous quarter. Some fields will have been removed however, such as commentary and narrative fields which are intended to be populated from scratch each time.

datamap
++++++++

The ``datamap`` is a crucual file that provides the link between the master database and the ``bicc_template.xlsx``.

The ``datamap`` file is of the form:

::

    *FIELD NAME,MASTER_SPREADSHEET_SHEET_NAME,CELL_REFERENCE,*

    for example:

    Project/Programme Name,Summary,B5,
    SRO Sign-Off,Summary,B49,
    ...

The file provides the 'map' between the ``master.csv`` and the ``bicc_template.xlsx``. This file is *HUMAN-CREATED* and requires the system administrator to indicate which CELL_REFERENCE in the ``bicc_template.xlsx`` file is populated by which FIELD_NAME in the ``master.csv``.

Populating BICC Return Forms from Master
----------------------------------------

TODO

Compiling Returned BICC Return Forms
-------------------------------------

Completed BICC return forms (in their native .xlsx format) should be copied into the ``[bcompiler]/source/returns`` folder.

To create a new master csv spreadsheet comprising the data from these returns, run:

``bcompiler --compile-to-master``

If the xlsx files are not copied to the correct folder (see above), the program will throw a FileNotFound error. A new ``compiled_master_DATE_QUARTER-REF.xlsx`` file will be created in ``[bcompiler]/output/``.


Overall Process
----------------

DIAGRAM HERE
