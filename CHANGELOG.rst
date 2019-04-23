rbackup Changelog
=================

Version 0.5.3
-------------

* rbackup.rsync
  * Log at the exception level, not at the library level
* rbackup.config.config_files
  * load_list_from_option()
    * Use non-mutable default argument
    * Ensure that list is returned if fallback is unset
* rbackup.struct.repository.Repository
  * Implement __eq__(), __ne__(), and __hash__()
  * Update docstrings explaining what happens to snapshot_symlink when snapshot is deleted
* Building
  * Add sphinx build commands to setup.py
  * Explain replacing colons on datetime on default snapshot name
* Project Structure
  * Move config module to config/config_files
  * Move config files to config_files/ in root dir
  * Delete rbackup.plugins.pacman module

Version 0.5.2
-------------

* Use try..finally blocks within context manager functions

Version 0.5.1
-------------

Bug Fixes
^^^^^^^^^

* backup script
   * Fix uninitialized repo variable

Version 0.5
-----------

* backup script
  * If rsync process fails, exit by its return code
* rbackup.struct.repository.Repository
  * Add basic logic for updating symlink after snapshot removal
