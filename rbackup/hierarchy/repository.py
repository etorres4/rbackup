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


# ========== Constants ==========
DIRMODE = 0o755
FILEMODE = 0o644


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
    * metadata_path (inherited from Hierarchy)
    * current_snapshot - either the most recent snapshot
        before running create_snapshot() or the new snapshot
        created after running create_snapshot()
    * snapshots - a list of snapshots stored in this repository
    * snapshot_dir - the snapshot storage location of this repository

    Methods
    -------
    * create_snapshot - create a new snapshot, then update current_snapshot
    * gen_snapshot_path - generate a path for a snapshot given by name
    * read_metadata (inherited from Hierarchy)
    * write_metadata (inherited from Hierarchy)

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

        if not self.metadata_path.exists():
            self._data = {"snapshots": [], "current_snapshot": None}
            self._init_new_repository()
        else:
            self._data = self.read_metadata()

    def _init_new_repository(self):
        """Perform the setup steps for a new repository."""
        self.metadata_path.parent.mkdir(mode=DIRMODE, exist_ok=True)
        self.metadata_path.touch(mode=FILEMODE)

        self.write_metadata()

    def __len__(self):
        """Return the number of snapshots in this Repository."""
        return len(self._data["snapshots"])

    def __getitem__(self, position):
        """Retrieve a Snapshot at a certain index."""
        return self.data["snapshots"][position]

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
            result = self._data["snapshots"][self._snapshot_index]
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
        >>> repo = Repository('backup')
        >>> repo.snapshot_dir # doctest: +ELLIPSIS
        PosixPath('backup/data')

        :rtype: path-like object
        """
        return self.path / "data"

    def gen_snapshot_path(self, name):
        """Generate a path for a Snapshot by name.

        Example
        -------
        >>> repo = Repository('backup')
        >>> repo.gen_snapshot_path('new-snapshot') # doctest: +ELLIPSIS
        PosixPath('backup/data/new-snapshot')

        :param name: name of the Snapshot
        :type name: str or path-like object
        :rtype: path-like object
        :raises: ValueError if name contains slashes
        """
        if "/" in str(name):
            raise ValueError("Names cannot contain slashes")

        return self.snapshot_dir / name

    @property
    def snapshots(self):
        """Return a list of snapshots stored in this Repository.

        Example
        -------
        >>> repo = Repository('backup')
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
        return self._data["snapshots"]

    @property
    def empty(self):
        """Determine whether or not this Repository is empty.

        Example
        -------
        >>> repo = Repository('backup')
        >>> repo.empty
        True
        >>> repo.create_snapshot() # doctest: +ELLIPSIS
        <...Snapshot ... at 0x...>
        >>> repo.empty
        False

        :rtype: bool
        """
        return self._data["snapshots"] == []

    @property
    def current_snapshot(self):
        """Return this Repository's current snapshot.

        :rtype: Snapshot object
        """
        return self._data["current_snapshot"]

    def create_snapshot(self, name=None):
        """Create a new snapshot in this repository.

        This method is non-intrusive in that it will not
        make any changes in the filesystem when called.

        :param name: the name of the snapshot
        :type name: str
        :return: a new Snapshot object
        :raises: FileExistsError if snapshot directory already exists
        """
        syslog.debug("Creating snapshot")

        snapshot_name = (
            name
            if name is not None
            else datetime.datetime.utcnow().isoformat().replace(":", "_")
        )
        self._data["current_snapshot"] = Snapshot(self.gen_snapshot_path(snapshot_name))
        self._data["snapshots"].append(self._data["current_snapshot"])

        self.write_metadata()

        try:
            self._data["current_snapshot"].path.mkdir(mode=DIRMODE, parents=True)
        except FileExistsError as e:
            raise e

        syslog.debug("Snapshot created")
        syslog.debug(f"Snapshot name: {self.current_snapshot.name}")

        return self._data["current_snapshot"]


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
