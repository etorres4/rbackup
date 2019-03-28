"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.repository
    :synopsis: Class for structuring a backup repository.
"""
import logging
import datetime
import pickle

from rbackup.hierarchy.hierarchy import Hierarchy
from rbackup.hierarchy.snapshot import Snapshot


# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Classes ==========
class Repository(Hierarchy):
    """A class for interacting with a backup repository.

        Repository is a mutable, stateful class for representing a
        directory that contains backup data sequestered into snapshots
        and a symlink to the most recently created snapshot.
    * Each snapshot in a repository is unaware of one another,
      this is the job of the repository to organize
    * The only way snapshots are linked together is in files
      that are hardlinked together

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
    * current_snapshot - either the most recent snapshot
        before running create_snapshot() or the new snapshot
        created after running create_snapshot()
    * snapshots - a list of snapshots stored in this repository
    * snapshot_dir - the snapshot storage location of this repository

    Methods
    -------
    * create_snapshot() - create a new snapshot, then update current_snapshot

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

        self._snapshot_index = 0

        if self._metadata_path.exists():
            with self._metadata_path.open(mode="rb") as metadata_file:
                self._snapshots = pickle.load(metadata_file)
        else:
            self._snapshots = []

        try:
            self._current_snapshot = self.snapshots[-1]
        except IndexError:
            self._current_snapshot = None

    def __len__(self):
        """Return the number of snapshots in this Repository."""
        return len(self.snapshots)

    def __getitem__(self, position):
        """Retrieve a Snapshot at a certain index."""
        return self.snapshots[position]

    def __delitem__(self, s):
        """Delete a Snapshot in this Repository."""
        raise NotImplementedError

    def __iter__(self):
        return self

    def __contains__(self, snapshot):
        """Check whether a Snapshot is in this Repository."""
        raise NotImplementedError

    def __next__(self):
        """Return the next Snapshot in this Repository."""
        try:
            result = self.snapshots[self._snapshot_index]
            self._snapshot_index += 1
            return result
        except IndexError:
            raise StopIteration

    @property
    def snapshot_dir(self):
        """Return the directory in this Repository in which snapshots
        are stored.

        Example
        -------
        >>> repo = Repository('/tmp')
        >>> repo.snapshot_dir # doctest: +ELLIPSIS
        PosixPath('/tmp/data')

        :rtype: path-like object
        """
        return self.path / "data"

    @property
    def snapshots(self):
        """Return a list of snapshots stored in this Repository.

        Example
        -------
        >>> repo = Repository('/tmp')
        >>> repo.snapshots
        []
        >>> repo.create_snapshot() # doctest: +ELLIPSIS
        <...Snapshot ... at 0x...>
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
        >>> repo.create_snapshot() # doctest: +ELLIPSIS
        <...Snapshot ... at 0x...>
        >>> repo.empty
        False

        :rtype: bool
        """
        return self.snapshots == []

    @property
    def current_snapshot(self):
        """Return this Repository's current snapshot.

        :rtype: Snapshot object
        """
        return self._current_snapshot

    def create_snapshot(
        self, name=datetime.datetime.utcnow().isoformat().replace(":", "-")
    ):
        """Create a new snapshot in this repository.

        This method is non-intrusive in that it will not
        make any changes in the filesystem when called.

        :return: a new Snapshot object
        """
        syslog.debug("Creating snapshot")

        if not isinstance(name, str):
            raise ValueError(f"{name} is not a valid type for a snapshot name")

        snapshot_name = (
            name
            if name is not None
            else datetime.datetime.utcnow().isoformat().replace(":", "-")
        )
        path = self.snapshot_dir / f"snapshot-{snapshot_name}"

        self._current_snapshot = Snapshot(path)
        self.snapshots.append(self._current_snapshot)

        syslog.debug("Snapshot created")
        syslog.debug(f"Snapshot name: {self.current_snapshot.name}")

        return self._current_snapshot


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
