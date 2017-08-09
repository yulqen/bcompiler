BCompiler
=========

.. contents::
    :depth: 2
    :backlinks: top
    :local:

Quick Start
-----------

* Clone the project (or download the zip file)
* pip install -r requirements
* Run setup.py


Introduction
-------------

``bcompiler`` is a tool manage data involved in the BICC reporting process at DfT. It is designed to provide a basic data processing function and making storing, cleaning and analysing the data historically contained in MS Excel files easier to manage.

It is currently a command line-only tool but future versions may involve a GUI or web interface.

``bcompiler`` performs to types of jobs: **populating** and **compiling**.

Known bugs and issues
--------------------
* You cannot paste commentary text into a master spreadsheet and expect to
  export cleanly back into templates. This is due to the potential for
  introducting non-friendly characters to the CSV process (newlines, commas,
  for instance).

