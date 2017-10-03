bbompiler
=========

.. contents::
    :depth: 2
    :backlinks: top
    :local:

Quick Start
-----------

* Ensure Python 3.6.2 is installed on your system.
* `pip install git+https://git@bitbucket.org/mrlemon/bcompiler.git`
* `bcompiler --help`

Alternatively:

* Clone the project (or download the zip file)
* pip install -r requirements.txt
* Run `python setup.py`


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

1. In command window, type `python -m pip install -U pip`.


Install git:

1. Go to https://git-scm.com/download/win. The download will begin
   automatically. Save it to a location on your hardrive, such as your Desktop
   or Downloads folder.
2. Run the installer, accepting all default options. If you get a message
   saying that you cannot run the 64-bit installer, choose the 32-bit installer
   from the above page.

Install bcompiler:

1. In command window, type `pip install git+https://git@bitbucket.org/mrlemon/bcompiler.git`

Known bugs and issues
--------------------
* You cannot paste commentary text into a master spreadsheet and expect to
  export cleanly back into templates. This is due to the potential for
  introducting non-friendly characters to the CSV process (newlines, commas,
  for instance).

