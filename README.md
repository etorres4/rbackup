[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# rbackup - An rsync-based backup tool

Yet another rsync-based tool for automating backups and using plugins.

## Rationales

- \'Keep It Simple Stupid\'
- Automate as much of the process as possible. This includes options,
  path selections, and managing snapshots
- Store backups in a format that does not require a program or script;
  this means that backups can be browsed with a file manager
- Deleted files are kept in old snapshots and rotated out using the
  rotation script
- Subsequent backups do not touch each other, unless specified by the
  user. This reduces the risk of overwriting backups with corrupted
  files

## Features

- Snapshot-based backup management
- Creation of installed package lists and archives of package manager
  databases
- AppArmor profiles

### Advanced Features

- rbackup depends on the filesystem that stores the repository to
  provide features such as checksumming, deduplication, and data
  integrity verification
- Encryption must be handled by an external program, this is out of
  scope for rbackup
- xattrs and acl\'s are handled by rsync but must be a supported
  feature of the filesystem the repository is stored on

## Target Directories

- /boot/loader
- /etc
- /home
- /root
- /var
  - /var/lib
  - /var/log
- Plugins
  - Installed packages
  - Package manager databases

## Backup Directory Hierarchy

    Repository
      current -> data/snapshot2
      data
        snapshot1
          .metadata
        snapshot2
          .metadata
      .metadata

Assuming snapshot2 was the most recent backup and snapshot1 was the
backup before that:

> - \"current\" would link to snapshot2
> - Unchanged files files from snapshot1 backed up to snapshot2 are
>   hardlinked to snapshot1

## Implementation Notes

- pathlib is used for path handling
- When hardlinking, rbackup passes the entire path to avoid needing
  relative paths
- The backup script changes the process umask to 0000

## To-do

- Create a separate backup and network backup script
  - Think about using `python-daemon` for `backupd`
  - rbackup.script: add `do_remote_backup` function
- Add \_\_enter\_\_ and \_\_exit\_\_ for PackageManager lockfiles to
  prevent transactions during backup
- Create snapshot manipulation script
- Interactive cleanup script
  - Repository.\_\_delitem\_\_()
  - Reconfiguring Repository.snapshot_symlink whenever a snapshot is
    deleted
- Plugin API
  - Plugin.run() and Plugin.communicate() abstract methods
    - Plugin.run() is passed a set of specific arguments
      - snapshot?
- \--dry-run touches the repository, change to make sure it doesn\'t

## Dependencies

### Runtime

- python\>=3.7
- rsync

### Build/Testing

- pytest
- setuptools
- hypothesis

#### License

This project is licensed under MIT. See LICENSE for more details.
