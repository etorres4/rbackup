.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

rbackup - An rsync-based backup tool
====================================
A tool that automates backup, file list parsing, snapshot creation, and hard-linking of files.

Features
--------
* Snapshot-based backup management
* Backups of deleted and modified files

Target Directories
------------------
* /boot
* /etc
* /home
* /root
* /var
  * /var/lib
  * /var/log
* Extras
  * Installed packages
  * Package manager databases

Backup Directory Hierarchy
--------------------------
* basedir
  | - data *directory containing all snapshots*
  |   | - snapshot1 *first snapshot*
  |     | - boot
  |     | - home
  |     | - etc
  |   | - snapshot2
  |     | - boot
  |     | - home
  |     | - etc
  | - prev *link to previous snapshot*
* Assuming snapshot2 was the previous backup and snapshot1 was the backup before that:
  * prev would link to snapshot2
  * Unchanged files files from snapshot1 backed up to snapshot2 are hardlinked to snapshot1


Implementation Notes
--------------------
* os.path is used for path handling
* Use --link-dest=
* Use --suffix=, --backup, and --backup-dir=

To-do
-----
* Use --suffix=, --backup, and --backup-dir=
