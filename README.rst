BCompiler
=========

Introduction
------------

``bcompiler`` is a tool manage data involved in the BICC reporting process at DfT. It is designed to provide a basic data processing function and making storing, cleaning and analysing the data historically contained in MS Excel files easier to manage.

It is currently a command line-only tool but future versions may involve a GUI or web interface.

``bcompiler`` performs to types of jobs: **populating** and **compiling**.

Populating
^^^^^^^^^^

**Populating** describes pulling data from a *master database* or spreadsheet into *multiple Excel files* for distribution to others.

Compiling
^^^^^^^^^

**Compiling** describes collating data from *multiple separate Excel files* into a *master database* or spreadsheet for storing the data and using as the basis for subsequent analysis.

The following table provides a summary of the main tasks:

+------------------------+-----------------------+
| Populating             | Compiling             |
+========================+=======================+
|Master to BICC Returns  | BICC Returns to Master|
+-----------------------+------------------------+
| Master to GMPP Return |                        |
+-----------------------+------------------------+

Working Directory
-----------------

BCompiler's job is to process external files, therefore it a directory in which to hold these files, as well as directories for output.

By default, this main directory intended to hold these external files is at:

``~/Documents/bcompiler`` (or equivalent on Windows)

how it is **not** created automatically unless the user directs this. Therefore the first action should be to create this directory using:

``bcompiler --create-wd``

If the directory currently exists, this will be reported to you. As you may have existing files in the working diretory which are key to the job at hand (such as a ``datamap`` file or a ``master.csv`` file), BCompiler will leave the directory untouched. However, if you wish to delete old working files and start from scratch, you may issue:

``bcompiler --force-create-wd`` which will remove the old directory and create a clean one.

Once you have created the requisite folder structure, you must then ensure the correct source files have been deposited in the ``bcompiler/source/``.

The following files are required for the purposes of populating (*Master to BICC* or *Master to GMPP*):

- master.csv                (a CSV version of the master spreadsheet)
- bicc_template.xlsx        (a blank BICC Return template in Excel)
- datamap                   (a comma-separated datamap file linking cell)

master.csv
++++++++++

This file can be created manually or could be the output from a *BICC Returns to Master* compilaton process. The traditonal structure for this file was a reverse-csv format, such as:

::

    Project/Programme Name,A14 Road Reconstruction,A303 Layby Maintenance,..
    Classification,DfT-102,DfT-102,..
    SRO Name,Jim Smith,Carol Heggarty,...
    SRO Training,SRO Master Practictioner,SRO Novice,...
    ...

Compiling Returned BICC Forms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Completed BICC return forms (in their native .xlsx format) should be copied into the ``[bcompiler]/source/returns`` folder.

To create a new master csv spreadsheet comprising the data from these returns, run:

``bcompiler --compile-to-master``

If the xlsx files are not copied to the correct folder (see above), the program will throw a FileNotFound error. A new ``compiled_master_DATE_QUARTER-REF.xlsx`` file will be created in ``[bcompiler]/output/``.
