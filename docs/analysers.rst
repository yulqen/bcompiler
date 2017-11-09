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

Available to all analysers
:::::::::::::::::::::::::::

* ``--master PATH_TO_DIRECTORY_CONTAINING_MASTER``


Available to swimlane_milestones analyser
:::::::::::::::::::::::::::::::::::::::::

The default is chart milestones within a range of 365 days from today. However,
the following options are available to give greater control to this band:

* ``--output PATH_TO_OUTPUT_DIRECTORY``
* ``--start_date DATE (dd/mm/yyyy)``
* ``--end_date DATE (dd/mm/yyyy)``

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

keyword
+++++++

Search for a keyword in the master key column (Column A) (e.g. RAG, or SRO). By default,
outputs to terminal.

.. topic:: Default

    ``>> bcompiler --analyser keyword "RAG"``

    Default options require a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file.

    Output is sent to your terminal.

    .. warning::
        Terminal output will exceed 80 characters. If you are using Windows, you
        should go to Preferences in ``cmd`` application and increase the width of
        the terminal window to something like 150 characters.

.. topic:: Output to xlsx (Excel) file

    ``>> bcompiler --analyser keyword "RAG" --xlsx C:\Users\jim\Desktop\rag.xlsx``

    This options requires a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file.
    The data is output to the file specified after the ``--xlsx`` flag, in this case ``C:\Users\jim\Desktop\rag.xlsx``.

.. topic:: Output to xlsx (Excel) and get data from a specific master

    ``>> bcompiler --analyser keyword "RAG" --xlsx C:\Users\jim\Desktop\rag.xlsx --master C:\Users\jim\Downloads\q1_master.xlsx``

    This options requires a master file to be present in the ``C:\Users\jim\Downloads`` directory, named ``q1_master.xlsx``.
    The data is output to the directory specified after the ``--output`` flag, in this case ``C:\Users\jim\Desktop\rag.xlsx``.

annex
+++++

Creates individual project spreadsheets pulling out pertinent headline and
textual data from a master. Intended to be used a Annex to BICC report. The
analyser relies on two master files to be present: a master representing
current data and one representing historical data. This is to allow for annex
to report a "DCA Last Quarter" value.

.. topic:: Default

    ``>> bcompiler --analyser annex``

    Default options require a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file, and
    a second master file, perhaps representing the previous quarter, named
    ``compare_master.xlsx`` in the same directory. You can use different
    filenames but this must be reflected in ``[MasterForAnalysis]`` and
    ``[AnalyserAnnex]`` in ``config.ini``.

.. topic:: Set compare master manually (overriding value in ``config.ini``)

    ``>> bcompiler --analyser annex --compare
    C:\Users\jim\Desktop\q1_master.xlsx``

.. topic:: Set output directory manually (overriding default of Documents/bcompiler/output

    ``>> bcompiler --analyser annex --output C:\Users\jim\Desktop``

    This options requires a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file.
    The files are output to the directory specified after the ``--output`` flag,
    in this case ``C:\Users\jim\Desktop``.
    
.. topic:: Set output directory manually (overriding default output directory of Documents/bcompiler/output and master set in ``config.ini``

    ``>> bcompiler --analyser annex --output C:\Users\jim\Desktop --master C:\Users\jim\Downloads\q1_master.xlsx``

    This options requires a master file to be present in the ``C:\Users\jim\Downloads`` directory, named ``q1_master.xlsx``.
    The files are output to the directory specified after the ``--output`` flag,
    in this case ``C:\Users\jim\Desktop``.

.. topic:: Set target master manually (overriding default set in ``config.ini``)

    ``>> bcompiler --analyser annex --master C:\Users\jim\Downloads\q1_master.xlsx``

    This options requires a master file to be present in the ``C:\Users\jim\Downloads`` directory, named ``q1_master.xlsx``.
    The files are output to ``Documents/bcompiler/output`` directory.

.. _swimlane-milestones:

swimlane_milestones
+++++++++++++++++++

Specific analyser uses project data from a master file and creates a new Excel
scatter chart, showing a timeline of major **approval** milestones horizontally in swimlane
fashion.

.. note::
    Basic configuration for milestones analysers is done in ``config.ini``.
    Documentation for these is contained in comments in the file.

.. topic:: Default options

    ``>> bcompiler --analyser swimlane_milestones``

    Default options require a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file.
    The chart is output in a file called ``swimlane_milestones.xlsx`` in the
    ``Documents/bcompiler/output`` directory.

    By default, the analyser will chart only those milestones that fall within 365
    days of today. This can be changed in ``config.ini`` by changing the ``range``
    value in the ``['AnalyserSwimlane']`` section.

.. topic:: Set output directory manually (overriding default of Documents/bcompiler/output

    ``>> bcompiler --analyser swimlane_milestones --output C:\Users\jim\Desktop``

    This options requires a master file to be present in the ``Documents/bcompiler`` directory, named ``target_master.xlsx`` as per the ``config.ini`` file.
    The chart is output to the directory specified after the ``--output`` flag,
    in this case ``C:\Users\jim\Desktop``.
    
.. topic:: Set output directory manually (overriding default output directory of Documents/bcompiler/output and master set in ``config.ini``

    ``>> bcompiler --analyser swimlane_milestones --output C:\Users\jim\Desktop --master C:\Users\jim\Downloads\q1_master.xlsx``

    This options requires a master file to be present in the ``C:\Users\jim\Downloads`` directory, named ``q1_master.xlsx``.
    The chart is output to the directory specified after the ``--output`` flag,
    in this case ``C:\Users\jim\Desktop``.

.. topic:: Set target master manually (overriding default set in ``config.ini``)

    ``>> bcompiler --analyser swimlane_milestones --master C:\Users\jim\Downloads\q1_master.xlsx``

    This options requires a master file to be present in the ``C:\Users\jim\Downloads`` directory, named ``q1_master.xlsx``.
    The chart is output to ``Documents/bcompiler/output`` directory.

.. topic:: Set start and end date

    ``>> bcompiler --analyser swimlane_milestones --start_date 20/1/2016 --end_date
    20/1/2017``

swimlane_assurance_milestones
+++++++++++++++++++++++++++++

As :ref:`swimlane-milestones` but showing **assurance** milestones.

