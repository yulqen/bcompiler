BCompiler
=========

Introduction
------------

This is the start of a README for BCompiler tool. A tool.

Working Directory
^^^^^^^^^^^^^^^^^

BCompiler's job is to process external files, therefore it a directory in which to hold these files, as well as a directory for output.

By default, this directory is at:

`~/Documents/bcompiler`

how it is **not** created automatically unless the user directs this. Therefore the first action should be to create this directory using:

`bcompiler --create-wd`

If the directory currently exists, this will be reported to you. As you may have existing files in the working diretory which are key to the job at hand (such as a `datamap` file or a `master.csv` file), BCompiler will leave the directory untouched. However, if you wish to delete old working files and start from scratch, you may issue:

`bcompiler --force-create-wd` which will remove the old directory and create a clean on.



