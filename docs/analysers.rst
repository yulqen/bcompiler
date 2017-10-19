Analysers
=========

Introduction
^^^^^^^^^^^^

``bcompiler`` is able to conduct basic analysis on spreadsheets. An analyser will usually process some data in a master spreadsheet and produce another spreadsheet (CSV, Excel), an Excel chart or some other data type.

Built-in analysers can be used in **two** ways: from the command line, or importing into your own Python programs.

To run the 'swimlane' analyser from the commandline:

>>> bcompiler --analyser swimlane

.. hint::
    Please see :ref:`Running analysers from the commandline` for all available flags.

To use 'swimlane' in your own code:

.. code-block:: python

    from bcompiler.analysers import Swimlane

    s = Swimlane()
    s.output('/home/user/Desktop/swimlane_output.xlsx')
    s.add_to_worksheet(worksheet)
    workbook.save()


.. hint::
    This is a hint

Built-in Analysers
^^^^^^^^^^^^^^^^^^

.. _Running Analysers From the CommandLine:

flags









