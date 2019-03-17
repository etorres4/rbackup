"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.repository
    :synopsis: Class for structuring a backup repository.
"""

import os.path
import datetime
import glob

from rbackup.hierarchy.hierarchy import Hierarchy
from rbackup.hierarchy.snapshot import Snapshot


class Repository(Hierarchy):
    """A class for interacting with a backup repository.

    At the time of creation, the following is true about the class:
    ===============================================================

    The current snapshot points to:
    -------------------------------
    * None if the repository is empty
    * The most recent snapshot before running create_snapshot()
    * A new, empty snapshot after running create_snapshot()

    Attributes
    ----------
    * path (inherited from Hierarchy)
    * curr_snapshot - return either the most recent snapshot
        before running create_snapshot() or the new snapshot
        created after running create_snapshot()
    * snapshots - return a list of snapshots stored in this repository

    Methods
    -------
    * create_snapshot() - create a new snapshot, then update curr_snapshot
    * update_snapshots() - update the list of snapshots this repository
        contains

    Directory Structure
    -------------------
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

        self._snapshot_dir = os.path.join(self.path, "data")
        self.update_snapshots()

        if self._snapshots == []:
            self._curr_snapshot = None
        else:
            self._curr_snapshot = self._snapshots[-1]

    @property
    def snapshots(self):
        """Return a list of snapshots stored in this Repository.

        Example
        -------
        >>> repo = Repository('/tmp')
        >>> repo.snapshots
        []
        >>> repo.create_snapshot()
        >>> repo.snapshots # doctest: +ELLIPSIS
        [<...Snapshot ... at 0x...>]

        :returns: the names of all snapshots in this repository sorted by
            date
        :rtype: list of Snapshot objects
        """
        return self._snapshots

    @property
    def empty(self):
        """Determine whether or not this Repository is empty.

        Example
        -------
        >>> repo = Repository('/tmp')
        >>> repo.empty
        True

        :rtype: bool
        """
        return self._snapshots == []

    @property
    def curr_snapshot(self):
        """Return this Repository's current snapshot.

        Example
        -------
        >>> repo = Repository('/tmp')
        >>> repo.curr_snapshot
        >>> repo.snapshots
        []
        >>> repo.create_snapshot()
        >>> repo.snapshots # doctest: +ELLIPSIS
        [<...Snapshot ... at 0x...>]
        >>> repo.curr_snapshot # doctest: +ELLIPSIS
        <...Snapshot ... at 0x...>

        :rtype: Snapshot object
        """
        return self._curr_snapshot

    def create_snapshot(
        self, name=datetime.datetime.utcnow().isoformat().replace(":", "-")
    ):
        """Create a new snapshot in this repository.

        This method is non-intrusive in that it will not
        make any changes in the filesystem when called.

        Example
        -------
        directive   ::= "#" "doctest":" ELLIPSIS
        >>> repo = Repository('/tmp')
        >>> repo.snapshots
        []
        >>> repo.curr_snapshot
        >>> repo.create_snapshot()
        >>> repo.curr_snapshot # doctest: +ELLIPSIS
        <...Snapshot ... at 0x...>

        :return: a new Snapshot object
        """
        path = os.path.join(self._snapshot_dir, f"snapshot-{name}")

        self._curr_snapshot = Snapshot(path)
        self._snapshots.append(self._curr_snapshot)

    def update_snapshots(self):
        """Update the list of snapshots in this repository."""
        self._snapshots = [
            Snapshot(s)
            for s in glob.glob(f"{self._snapshot_dir}/*")
            if os.path.isdir(s)
        ]


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()