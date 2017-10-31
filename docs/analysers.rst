Analysers
=========

Introduction
^^^^^^^^^^^^

``bcompiler`` is able to conduct basic analysis on spreadsheets. An analyser will usually process some data in a master spreadsheet and produce another spreadsheet (CSV, Excel), an Excel chart, commandline output, or some other data type.

Built-in analysers can be used in **two** ways:

* from the command line
* importing into your own Python programs
  
Analysers available from the commandline use mostly default options and are relatively limited. More extensive configuration can be gained by writing your own scripts and importing bcompiler analyser code into your project to help you. See :ref:`importing-analyser-code` for more details.


Running from the commandline
++++++++++++++++++++++++++++

Basic command
~~~~~~~~~~~~~~

``>> bcompiler --analyser ANALYSER OPTIONS``



Available options
~~~~~~~~~~~~~~~~~~

* ``--output PATH_TO_OUTPUT_DIRECTORY``
* ``--master PATH_TO_DIRECTORY_CONTAINING_MASTER``

.. hint::
    Please see :ref:`commandline-examples` for examples of running an analyser
    from the commandline.

.. _importing-analyser-code:

Importing analyser code into your own projects
+++++++++++++++++++++++++++++++++++++++++++++++

.. warning::
    This functionality is not yet implemented.

.. code-block:: python

    from bcompiler.analysers import Swimlane

    s = SwimlaneMilestones()
    s.output('/home/user/Desktop/swimlane_milestones.xlsx')
    s.add_to_worksheet(worksheet)
    workbook.save()


Built-in Analysers
^^^^^^^^^^^^^^^^^^

annex
+++++

Creates individual project spreadsheets pulling out pertinent headline and
textual data from a master. Intended to be used a Annex to BICC report.

Example: Default options
~~~~~~~~~~~~~~~~~~~~~~~~~

``>> bcompiler --analyser annex``

.. note::
    Default options require a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file.

Example: Set output directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``>> bcompiler --analyser annex --output C:\Users\jim\Desktop``

.. note::
    This options requires a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file.
    The files are output to the directory specified after the ``--output`` flag,
    in this case ``C:\Users\jim\Desktop``.
    
Example: Set output directory and target master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``>> bcompiler --analyser annex --output C:\Users\jim\Desktop --master C:\Users\jim\Downloads\q1_master.xlsx``

.. note::
    This options requires a master file to be present in the ``C:\Users\jim\Downloads`` directory, named ``q1_master.xlsx``.
    The files are output to the directory specified after the ``--output`` flag,
    in this case ``C:\Users\jim\Desktop``.

Example: Set target master
~~~~~~~~~~~~~~~~~~~~~~~~~~

``>> bcompiler --analyser annex --master C:\Users\jim\Downloads\q1_master.xlsx``

.. note::
    This options requires a master file to be present in the ``C:\Users\jim\Downloads`` directory, named ``q1_master.xlsx``.
    The files are output to ``Documents/bcompiler/output`` directory.


swimlane_milestones
+++++++++++++++++++

Specific analyser uses project data from a master file and creates a new Excel
scatter chart, showing a timeline of major milestones horizontally in swimlane
fashion.


.. _commandline-examples:

Example: Default options
~~~~~~~~~~~~~~~~~~~~~~~~~

``>> bcompiler --analyser swimlane_milestones``

.. note::
    Default options require a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file.
    The chart is output in a file called ``swimlane_milestones.xlsx`` in the
    ``Documents/bcompiler/output`` directory.

Example: Set output directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``>> bcompiler --analyser swimlane_milestones --output C:\Users\jim\Desktop``

.. note::
    This options requires a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file.
    The chart is output to the directory specified after the ``--output`` flag,
    in this case ``C:\Users\jim\Desktop``.
    
Example: Set output directory and target master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``>> bcompiler --analyser swimlane_milestones --output C:\Users\jim\Desktop --master C:\Users\jim\Downloads\q1_master.xlsx``

.. note::
    This options requires a master file to be present in the ``C:\Users\jim\Downloads`` directory, named ``q1_master.xlsx``.
    The chart is output to the directory specified after the ``--output`` flag,
    in this case ``C:\Users\jim\Desktop``.

Example: Set target master
~~~~~~~~~~~~~~~~~~~~~~~~~~

``>> bcompiler --analyser swimlane_milestones --master C:\Users\jim\Downloads\q1_master.xlsx``

.. note::
    This options requires a master file to be present in the ``C:\Users\jim\Downloads`` directory, named ``q1_master.xlsx``.
    The chart is output to ``Documents/bcompiler/output`` directory.


