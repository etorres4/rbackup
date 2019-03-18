"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.repository
    :synopsis: Class for structuring a backup repository.
"""
import logging
import datetime

from rbackup.hierarchy.hierarchy import Hierarchy
from rbackup.hierarchy.snapshot import Snapshot


# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Classes ==========
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
    * name (inherited from Hierarchy)
    * curr_snapshot - return either the most recent snapshot
        before running create_snapshot() or the new snapshot
        created after running create_snapshot()
    * snapshots - return a list of snapshots stored in this repository

    Methods
    -------
    * create_snapshot() - create a new snapshot, then update curr_snapshot

    Directory Structure
    -------------------
    * "data" directory for storing snapshots
      * Each snapshot is its own directory with its own sub-hierarchy
      * Each snapshot has an "old" directory for storing deleted data
      * rsync hardlinks unchanged files between snapshots
    * A symlink in the root of the repository symlinking to the
      most recent snapshot

    Iteration
    ---------
    To support checking all snapshots for hardlinking, the Repository class
    can be iterated through.
    """

    def __init__(self, dest):
        """Default constructor for the Repository class."""
        super().__init__(dest)

        self._snapshot_dir = self.path / "data"
        self._snapshots = [
            Snapshot(s) for s in self._snapshot_dir.glob("*") if s.is_dir()
        ]

        if self._snapshots == []:
            self._curr_snapshot = None
        else:
            self._curr_snapshot = self._snapshots[-1]

    def __len__(self):
        """Return the number of snapshots in this Repository."""
        return len(self.snapshots)

    def __getitem__(self, position):
        """Retrieve a Snapshot at a certain index."""
        return self.snapshots[position]

    def __iter__(self):
        self.snapshot_index = 0
        return self

    def __next__(self):
        """Return the next Snapshot in this Repository."""
        try:
            result = self.snapshots[self.snapshot_index]
            self.snapshot_index += 1
            return result
        except IndexError:
            raise StopIteration

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
        >>> repo.create_snapshot()
        >>> repo.empty
        False

        :rtype: bool
        """
        return self.snapshots == []

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
        try:
            return self.snapshots[-1]
        except IndexError:
            return None

    def create_snapshot(
        self, name=datetime.datetime.utcnow().isoformat().replace(":", "-")
    ):
        """Create a new snapshot in this repository.

        This method is non-intrusive in that it will not
        make any changes in the filesystem when called.

        Example
        -------
        >>> repo = Repository('/tmp')
        >>> repo.snapshots
        []
        >>> repo.curr_snapshot
        >>> repo.create_snapshot()
        >>> repo.curr_snapshot # doctest: +ELLIPSIS
        <...Snapshot ... at 0x...>

        :return: a new Snapshot object
        """
        syslog.debug("Creating snapshot")
        path = self._snapshot_dir / f"snapshot-{name}"

        self._curr_snapshot = Snapshot(path)
        self.snapshots.append(self._curr_snapshot)

        syslog.debug("Snapshot created")
        syslog.debug(f"Snapshot name: {self.curr_snapshot.name}")


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
