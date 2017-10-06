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

``bcompiler`` is a tool manage data involved in the BICC reporting process at DfT. It is designed to provide a basic data processing function and making storing, cleaning and analysing the data historically contained in MS Excel files easier to manage.

It is currently a command line-only tool but future versions may involve a GUI or web interface.

``bcompiler`` performs to types of jobs: **populating** and **compiling**.

Installation (Windows)
----------------------

First, install Python:

1. To install Python, download installer file from
   http://www.python.org/ftp/python/3.6.2/python-3.6.2.exe. Choose to
   save it to a location on your harddrive, such as your Desktop or Downloads
   folder.
2. Run the installer. On the Install Python 3.6.2 Setup screen, ensure "Add
   Python 3.6 to PATH" and "Install launcher for all users (recommended)" is checked. Click "Install Now".
3. Open a new command window (Start -> type "cmd" in Search box and hit enter).

Update pip:

* In command window, type ``python -m pip install -U pip``.


Install git:

1. Go to https://git-scm.com/download/win. The download will begin
   automatically. Save it to a location on your hardrive, such as your Desktop
   or Downloads folder.
2. Run the installer, accepting all default options. If you get a message
   saying that you cannot run the 64-bit installer, choose the 32-bit installer
   from the above page.

Install bcompiler:

* In the command window, type ``pip uninstall bcompiler`` to uninstall any existing installation of
  ``bcompiler``. 
* In command window, type ``pip install bcompiler``, or if you choose not to remove ``bcompiler`` first (see point above), then type ``pip install -U bcompiler`` to upgrade to the latest version of ``bcompiler``.


Initialising bcompiler:

bcompiler needs some auxiliary files to run, including a ``datamap.csv`` and ``config.ini`` files. These files are stored in a directory called ``bcompiler`` in your ``Documents`` directory. Before running ``bcompiler``, this directory structure needs to be set up. The auxiliary files also need to be downloaded from a [git repository on Github](https://github.com/departmentfortransport/bcompiler_datamap_files). ``bcompiler`` can do the necessary work to set this up.

If you already have a  ``~/Documents/bcompiler`` (if using a Linux or Mac OSX machine) or ``MyDocuments\bcompiler`` (if using a Windows machine) directory, then you do not need to use the following command. If you DO have this directory in place already, running the following command will ask whether you want to delete this and refresh the auxiliary files from the remote repository.

To initialise bcompiler:

* In the command window, type ``bcompiler-init``.

**PLEASE NOTE:** Due to a bug in current version of ``bcompiler``, if you try to run ``bcompiler`` and you do not have the necessary auxiliary files installed, ``bcompiler`` will throw an error. Please ensure you run ``bcompiler-init`` first to set up the necessary files.

Known bugs and issues
--------------------
* See above
