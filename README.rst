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

Implementation Notes
--------------------
* os.path is used for path handling
* Use --link-dest=
* Use --suffix=, --backup, and --backup-dir=
