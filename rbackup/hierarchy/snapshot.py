"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy
    :synopsis: Classes for creating the backup hierarchy.
"""

import os.path


class Snapshot(Hierarchy):
    """Hierarchy for a single snapshot.

    Example
    -------
    >>> repo = Repository('backup')
    >>> snapshots = repo.snapshots
    >>> prev = snapshots[-1]
    >>> prev.name
    >>> 'snapshot-{prevtime}'
    >>> prev.home_dir
    >>> 'backup/data/snapshot-{prevtime}/home'
    >>> curr = repo.curr_snapshot
    >>> curr.name
    >>> 'snapshot-{utcnow}'
    >>> curr.home_dir
    >>> 'backup/data/snapshot-{utcnow}/home'
    """

    def __init__(self, path):
        """Default constructor for the Snapshot class."""
        super().__init__(path)

    @property
    def path(self):
        """Return the canonical path of this snapshot.
        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-{utcprev}')
        >>> s.name
        >>> 'backup/data/snapshot-{utcprev}'

        :rtype: str
        """
        return self.base_path

    @property
    def name(self):
        """Return the name of this snapshot.

        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-{utcprev}')
        >>> s.name
        >>> 'snapshot-{utcprev}'

        :rtype: str
        """
        return os.path.basename(self.base_path)

    @property
    def boot_dir(self):
        """Retrieve the /boot backup directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-{utcnow}')
        >>> s.boot_dir
        >>> 'backup/data/snapshot-{utcnow}/boot'

        :rtype: str
        """
        return os.path.join(self.base_path, "boot")

    @property
    def etc_dir(self):
        """Retrieve the /etc backup directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-{utcnow}')
        >>> s.etc_dir
        >>> 'backup/data/snapshot-{utcnow}/etc'

        :rtype: str
        """
        return os.path.join(self.base_path, "etc")

    @property
    def home_dir(self):
        """Retrieve the /home backup directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-{utcnow}')
        >>> s.home_dir
        >>> 'backup/data/snapshot-{utcnow}/home'

        :rtype: str
        """
        return os.path.join(self.base_path, "home")

    @property
    def root_home_dir(self):
        """Retrieve root's home directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-{utcnow}')
        >>> s.root_home_dir
        >>> 'backup/data/snapshot-{utcnow}/root'

        :rtype: str
        """
        return os.path.join(self.base_path, "root")
