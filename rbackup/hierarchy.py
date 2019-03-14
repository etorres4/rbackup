"""
.. author:: Eric Torres
.. module:: hierarchy
    :synopsis: Classes for creating the backup hierarchy.
"""

import os.path
import datetime
import glob


class Hierarchy:
    """A class for organizing the backup root hierarchy.
    See README.rst for more details."""

    def __init__(self, dest):
        """Default constructor for the Hierarchy class.

        :param dest: the root directory of the backup hierarchy
        :type dest: str, bytes
        :raises: NotADirectoryError if dest is not a directory
        """
        if not os.path.isdir(dest):
            raise NotADirectoryError(f"{dest}: no such directory")

        self.dest = dest

    @property
    def base_path(self):
        """Return the base directory of this hierarchy.

        >>> h = Hierarchy('backup')
        >>> h.base_path
        >>> 'backup'

        :rtype: str
        """
        return self.dest


class Repository(Hierarchy):
    """A class for interacting with a backup repository.

    Attributes
    ----------
    * "data" directory for storing snapshots
      * Each snapshot is its own directory with its own sub-hierarchy
      * Each snapshot has an "old" directory for storing deleted data
      * rsync hardlinks unchanged files between snapshots
    * A symlink in the root of the repository symlinking to the
      most recent snapshot
    """
    def __init__(self, dest):
        """Default constructor for the Repository class."""
        super().__init__(dest)

        self._snapshot_dir = os.path.join(self.base_path, "data")
        self._snapshots = [
            Snapshot(s)
            for s in glob.glob(f"{self._snapshot_dir}/*")
            if os.path.isdir(s)
        ]

    @property
    def snapshots(self):
        """Return a list of snapshots stored in this Repository.

        Example
        -------
        * Assuming that backup/data has the snapshot dirs:
          * snapshot-one
          * snapshot-two
        >>> repo = Repository('backup')
        >>> repo.snapshots
        >>> ['backup/data/snapshot-one', 'backup/data/snapshot-two']

        :returns: the names of all snapshots in this repository sorted by
            date
        :rtype: list
        :rtype: None if there are no snapshots in this Repository
        """
        if self._snapshots == []:
            return None
        else:
            return self._snapshots

    @property
    def prev_snapshot(self):
        """Return the instance of the previous Snapshot.

        :rtype: Snapshot object
        """
        if self._snapshots == []:
            return None
        else:
            return self.snapshots[-1]

    @property
    def curr_snapshot(self):
        """Create a new Snapshot object and return its handle.

        Example
        -------
        >>> repo = Repository('backup')
        >>> repo.curr_snapshot
        >>> Snapshot('backup/data/snapshot-{utcnow}')

        :rtype: Snapshot object
        """
        date = datetime.datetime.utcnow().isoformat().replace(":", "-")
        path = os.path.join(self._snapshot_dir, f"snapshot-{date}")

        return Snapshot(path)


class Snapshot(Hierarchy):
    """Hierarchy for a single snapshot.

    Example
    -------
    >>> repo = Repository('backup')
    >>> snapshots = repo.snapshots
    >>> prev = snapshots[-1]
    >>> prev.name
    >>> 'backup/data/snapshot-{prevtime}'
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
