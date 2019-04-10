"""
.. author:: Eric Torres
.. module:: rbackup.struct.repository
    :synopsis: Class for structuring a backup repository.
"""
import logging
import datetime

from rbackup.struct.hierarchy import Hierarchy
from rbackup.struct.snapshot import Snapshot


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

    def _is_duplicate_name(self, name):
        """Check whether or not a snapshot of a given name is already 
        on this Repository.

        If the repository is empty, then this method always returns False.

        :param name: the name to check for
        :returns: True if this name is already in a snapshot.
        :type name: str
        :rtype: bool
        """
        for s in self._data["snapshots"]:
            if name == s.name:
                return True
        return False

    def _is_valid_name(self, name):
        """Check if the given name is a valid name. If it is a duplicate,
        log a warning. If it is invalid, raise a ValueError.

        Invalid Names:
        --------------
        * Contain slashes
        * Are empty values i.e. '' or []

        :param name: name to validate
        :type name: str
        :returns: true if this name is deemed valid
        :rtype: bool
        """
        if not str(name) or "/" in name:
            return False
        else:
            return True

    def __len__(self):
        """Return the number of snapshots in this Repository."""
        return len(self._data["snapshots"])

    def __getitem__(self, position):
        """Retrieve a Snapshot at a certain index."""
        return self._data["snapshots"][position]

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

        :rtype: path-like object
        """
        return self.path / "data"

    @property
    def snapshots(self):
        """Return a list of snapshots stored in this Repository.

        :returns: the names of all snapshots in this repository sorted by
            date
        :rtype: list of Snapshot objects
        """
        return self._data["snapshots"]

    @property
    def empty(self):
        """Determine whether or not this Repository is empty.

        :rtype: bool
        """
        return self._data["snapshots"] == []

    @property
    def current_snapshot(self):
        """Return this Repository's current snapshot.

        :rtype: Snapshot object
        """
        return self._data["current_snapshot"]

    # TODO search for the name of snapshots
    # add ability to use 'in' operator
    def create_snapshot(self, name=None):
        """Create a new snapshot in this repository.

        This method is non-intrusive in that it will not
        make any changes in the filesystem when called.

        If name is given and it is the name of a snapshot already
        on the repository, that snapshot is overwritten instead.

        :param name: the name of the snapshot
        :type name: str
        :return: a new Snapshot object
        :raises: ValueError if name is an invalid value
        """
        syslog.debug("Creating snapshot")

        snapshot_name = (
            name
            if name is not None
            else datetime.datetime.utcnow().isoformat().replace(":", "_")
        )

        if not self._is_valid_name(snapshot_name):
            raise ValueError(f"{name} is an invalid name")
        elif self._is_duplicate_name(snapshot_name):
            syslog.warning("Snapshot already exists, data will be overwritten.")
        else:
            self._data["current_snapshot"] = Snapshot(self.snapshot_dir / snapshot_name)
            self._data["snapshots"].append(self._data["current_snapshot"])

        self.write_metadata()

        self._data["current_snapshot"].path.mkdir(
            mode=DIRMODE, parents=True, exist_ok=True
        )

        syslog.debug("Snapshot created")
        syslog.debug(f"Snapshot name: {self.current_snapshot.name}")

        return self._data["current_snapshot"]


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
