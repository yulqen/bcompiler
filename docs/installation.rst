Installation
------------

.. note::
    This guide refers specifically to installing on a Windows system as that is
    anticipated to be the primary operating system for typical ``bcompiler``
    users. However, ``bcompiler`` is installable on Linux and Mac using the
    same ``pip`` commands. The only difference is how Python and ``git`` are
    installed on those systems. Please refer to `python.org <https://www.python.org/downloads/mac-osx/>`_ and `git-scm.com <https://git-scm.com/>`_.

Install Python
+++++++++++++++++++++

1. To install Python, download installer file from
   http://www.python.org/ftp/python/3.6.2/python-3.6.3.exe. Choose to
   save it to a location on your harddrive, such as your Desktop or Downloads
   folder.
2. Run the installer. On the Install Python Setup screen, ensure "Add
   Python 3.6 to PATH" and "Install launcher for all users (recommended)" is checked. Click "Install Now".
3. Open a new command window (Start -> type "cmd" in Search box and hit enter).

Update pip (if required)
++++++++++++++++++++++++

* In command window, type ``python -m pip install -U pip``.


Install git
+++++++++++

1. Go to https://git-scm.com/download/win. The download will begin
   automatically. Save it to a location on your hardrive, such as your Desktop
   or Downloads folder.
2. Run the installer, accepting all default options. If you get a message
   saying that you cannot run the 64-bit installer, choose the 32-bit installer
   from the above page.

Install bcompiler
+++++++++++++++++

* If you do not already have ``bcompiler`` installed, in the command window, type ``pip install bcompiler``.
* If you have ``bcompiler`` installed, it is a good idea to update to the latest version. In the command window, type ``pip install -U bcompiler``.

.. note::
    **Use the latest version of bcompiler**. You can find out what the latest
    version of bcompiler is by doing ``pip search bcompiler``. If you can see
    that there is a later version, but ``pip install -U bcompiler`` does not
    install the latest version for some reason, try uninstalling bcompiler
    ``pip uninstall bcompiler`` first, then installing with ``pip install
    bcompiler``. You can also specify which version of ``bcompiler`` you want
    to download with ``pip install bcompiler==1.1.0a1`` - make sure that
    version is listed as the latest doing ``pip search bcompiler``.
