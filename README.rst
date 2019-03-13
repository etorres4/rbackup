.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

rbackup - An rsync-based backup tool
====================================

Features
--------
* Snapshot-based backup management
* Backups of deleted and modified files

Implementation Notes
--------------------
* os.path is used for path-handling
* Use --link-dest=
* Use --suffix=, --backup, and --backup-dir=

To-Do
-----
* rsync reads paths with a ':' as a remote host, do not do that

rsync --archive --prune-dirs --hard-links --verbose --link-dest='current_snapshot_dir' --recursive --ignore-missing-args --files-from /etc /backup_dir/etc
