.. _use:

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

