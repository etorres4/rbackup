.. rbackup documentation master file, created by
   sphinx-quickstart on Sun Apr 14 13:06:20 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to rbackup's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   rbackup
   rbackup.package_managers
   rbackup.struct

----------------------
Principle of Operation
----------------------

Each time the backup script for rbackup is run, it creates a new snapshot and runs a backup of included paths using rsync to that new snapshot. This ensures that backup data does not overwrite pre-existing data. Paths are included by including paths relative to ``/`` in files suffixed with ``-include.conf`` in  ``/etc/rbackup``.

The backup script follows this procedure:

1. Load specified repository and existing snapshots if any.
2. If specified repository is new, then set up metadata.
3. Create a new snapshot in the specified repository. If a name is specified, give the snapshot said name. If a snapshot with said name already exists, then overwrite that snapshot instead.
4. Aggregate all desired and excluded paths into two separate temporary files. Pass both files and default arguments to rsync.
5. Run the rsync process and wait until process is finished
6. If there is an existing symlink pointing to a snapshot in the repository, then delete it.
7. Create a symlink in the repository root directory pointing to the new snapshot.


-------------
Configuration
-------------

The directory for configuration files is /etc/rbackup.

Paths to include in the backup are included in ``*-include.conf`` files located in the configuration directory. Likewise, paths to exclude from the backup are in ``*-exclude.conf`` files in the same directory. The backup script automatically looks for and includes paths written in these files. Each path, whether include or exclude should be relative to the root directory (/).

For example, if the /etc/NetworkManager directory was desired for backup, one would write etc/NetworkManager in a file that could be named 'etc-include.conf' in /etc/rbackup. Users can separate different paths into multiple include files for organization.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
