Changelog for rbackup
=====================

Version 0.7
-----------

* backup script

  * Make ``backup`` strictly for backups to a local repository
  * Add description for script in help message

* Bug fixes

  * backup script

    * Fix incorrect log message handling
    * Add slash between port and hostname
    * Remove -v, --verbose flag

* Documentation

  * Change all instances of ``:returns:`` in docstrings to ``:return:``
  * Make mention of default kwargs values for all modules

* Project Structure

  * Split common logging operations into rbackup.logging module

Version 0.6
-----------

* backup script

  * Add --port option for ssh
  * Add --umask option for changing umask of backup process

* backupd

  * Add backupd script
  * Add config file

* rbackup.network

  * Add rbackup.network module

* rbackup.system

  * Add associated tests

* Building

  * Fix incorrect parameters on setup.py sphinx section

* Project Structure

  * Add ``rbackup.network``, ``rbackup.script``, and ``rbackup.system``
  * Split main backup script into separate library modules for easier maintainability
  

Version 0.5.3
-------------

* rbackup.rsync

  * Log at the exception level, not at the library level

* rbackup.config.config_files

  * ``load_list_from_option()``

    * Use non-mutable default argument
    * Ensure that list is returned if fallback is unset

* rbackup.struct.repository.Repository

  * Implement ``__eq__()``, ``__ne__()``, and ``__hash__()``
  * Update docstrings explaining what happens to snapshot_symlink when snapshot is deleted

* Building

  * Add sphinx build commands to ``setup.py``
  * Explain replacing colons on datetime on default snapshot name

* Project Structure

  * Move config module to ``rbackup.config.config_files``
  * Move config files to ``config_files/`` in root dir
  * Delete ``rbackup.plugins.pacman`` module

Version 0.5.2
-------------

* Use ``try..finally`` blocks within context manager functions

Version 0.5.1
-------------

Bug Fixes
^^^^^^^^^

* backup script

   * Fix uninitialized repo variable
   * If rsync process fails, exit by its return code

Version 0.5
-----------

* rbackup.plugins.package_managers.PackageManager

  * Raise ``NotimplementedError`` for non-supported operations

* rbackup.struct.hierarchy.Hierarchy

  * Move ``Repository.gen_metadata()`` to ``Hierarchy._gen_metadata()``

* rbackup.struct.repository.Repository

  * Add basic logic for updating symlink after snapshot removal
  * Implement snapshot deletion using ``__delitem__()``
  * Add basic logic for symlinking after snapshot removal

* rbackup.struct.repository.Snapshot

  * Add attribute code to ``_gen_metadata()``
  * Add ``ctime`` attribute

* Project structure

  * Add file for snapshot management script
  * Rename ``rbackup.package_managers`` to ``rbackup.plugins``

Version 0.4.1
-------------

* backup script

  * Change umask to ``0000`` when running backup

Version 0.4
-----------

* backup script

  * Use fallback option 

* rbackup.config Folder

  * Add ``[main]`` to default config file

* rbackup.config.config_files

  * Add ``load_list_from_option()``

Version 0.3
-----------

* rbackup.rsync

  * Add default rsync options list

* rbackup.struct.hierarchy.Hierarchy

  * Don't calculate private attributes each time they are called

* rbackup.struct.repository.Repository

  * Add ``gen_metadata()``
  * Add ``symlink_snapshot()``
  * Ignore ``PermissionError`` when creating snapshot symlink

* config_files

  * Include ``/root`` in default paths

* Split config file handling into its own module
* Doctest cleanup

Version 0.2
-----------

* rbackup.config

  * Merge, filter, and sort file entries from multiple files

* rbackup.rsync

  * Change execution of rsync subprocess to text mode

* rbackup.config_files

  * Split ``etc-include`` and ``system-include`` config files

* rbackup.package_managers.packagemanager.PackageManager

  * Remove type and value checking
  * Add ``gen_db_archive()``
  * Check for valid compression mode before proceeding with ``gen_db_archive()``

* rbackup.struct.hierarchy.Hierarchy

  * Add ``metadata_path``
  * Subclass ``os.PathLike``
  * Make write_metadata() an atomic operation
  * Log metadata read/write operations

* rbackup.struct.repository.Repository

  * Add ``cleanup()``
  * Add ``is_valid_snapshot_name()``
  * Add ``gen_snapshot_path()``
  * Remove current_snapshot attribute
  * Implement ``__repr__()``
  * Use regex to parse user snapshot name input
  * Split snapshot metadata lists
  * Change serialization backend from pickle to JSON
  * Raise ``ValueError`` when snapshot name contains a '/'

* rbackup.struct.repository.Snapshot

  * Remove all attributes except for ``pkg_dir``

* Project structure

  * Do not ship test suite under rbackup package
  * Rename ``rbackup.hierarchy`` package to ``rbackup.struct``

Version 0.1
-----------

* Initial commit
* Project structure

  * Add basic modules
  * Add LICENSE
