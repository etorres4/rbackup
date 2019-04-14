"""
.. author:: Eric Torres
.. module:: rbackup.struct.repository

:synopsis: Module for helpers for structuring a backup repository.
"""
import datetime
import logging
import re
import shutil

from rbackup.struct.hierarchy import Hierarchy
from rbackup.struct.snapshot import Snapshot

# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Constants ==========
DIRMODE = 0o755
FILEMODE = 0o644

VALID_SNAPSHOT_NAME = r"[\w._+-]+[^/]*"


# ========== Classes ==========
class Repository(Hierarchy):
    """A class for interacting with a backup repository.

        Repository is a mutable, stateful class for representing a
        directory that contains backup data sequestered into snapshots
        and a symlink to the most recently created snapshot.

    * Each snapshot in a repository is unaware of one another,
      this is the job of the repository to organize
    * The only way snapshots are linked together is in files
      that are hard-linked together

    Attributes
    ----------
    * Repository.path (inherited from Hierarchy)
    * Repository.name (inherited from Hierarchy)
    * Repository.metadata_path (inherited from Hierarchy)
    * Repository.snapshots - a list of snapshots stored in this repository
    * Repository.snapshot_dir - the snapshot storage location of this repository

    Methods
    -------
    * cleanup - clean all repository data
    * create_snapshot - create a new snapshot
    * gen_metadata (inherited from Hierarchy)
    * is_valid_snapshot_name - validate a potential name for a snapshot
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

    """Snapshots are serialized as their names relative to the repository
    data directory, but have their full paths during runtime.

    Private Attributes
    ------------------
    * _snapshots - list of Snapshot objects created and accessed at runtime
    * _snapshot_metadata - list of Snapshot names serialized and deserialized
        when this Repository is first created
    """

    def __init__(self, dest):
        """Default constructor for the Repository class.
        """
        super().__init__(dest)

        if not self.metadata_path.exists():
            self._snapshots = []
            self._snapshot_metadata = []
            self.metadata_path.parent.mkdir(mode=DIRMODE, exist_ok=True)
            self.metadata_path.touch(mode=FILEMODE)
            self.write_metadata(self._snapshots)
        else:
            self._snapshot_metadata = self.read_metadata()
            self._snapshots = [
                Snapshot(self.snapshot_dir / s) for s in self._snapshot_metadata
            ]

        self._snapshot_iterator = iter(self._snapshots)

    def __contains__(self, name):
        """Check whether a Snapshot is in this Repository by name.

        :type name: str
        :rtype: bool
        """
        return name in self._snapshot_metadata

    def __delitem__(self, s):
        """Delete a Snapshot in this Repository."""
        raise NotImplementedError

    def __getitem__(self, position):
        """Retrieve a Snapshot at a certain index."""
        return self._snapshots[position]

    def __iter__(self):
        return iter(self._snapshots)

    def __len__(self):
        """Return the number of snapshots in this Repository."""
        return len(self._snapshots)

    def __next__(self):
        """Return the next Snapshot in this Repository."""
        return next(self._snapshot_iterator)

    @staticmethod
    def is_valid_snapshot_name(name):
        """Check if the given name is a valid name.

        Invalid Names:
        --------------
        * Contain slashes
        * Are empty values

        Valid names match the regex
        r'[\\w]+[^/]*'

        :param name: name to validate
        :type name: str
        :returns: true if this name is deemed valid
        :rtype: bool
        """
        return bool(re.match(VALID_SNAPSHOT_NAME, name))

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
        return self._snapshots

    @property
    def empty(self):
        """Determine whether or not this Repository is empty.

        :rtype: bool
        """
        return not self.snapshots

    def gen_metadata(self):
        """Generate metadata for this repository.
            After this method is called, the data necessary for this snapshot has been created.
        """
        pass

    def create_snapshot(self, name=None):
        """Create a new snapshot in this repository.

        This method is non-intrusive in that it will not
        make any changes in the filesystem when called.

        If name is given and it is the name of a snapshot already
        on the repository, that snapshot is overwritten instead.

        :param name: the name of the snapshot
        :type name: str
        :return: Snapshot object
        :raises ValueError: if name is an invalid value
        """
        syslog.debug("Creating snapshot")

        snapshot_name = (
            name
            if name is not None
            else datetime.datetime.utcnow().isoformat().replace(":", "_")
        )

        if not self.is_valid_snapshot_name(snapshot_name):
            raise ValueError(f"'{name}' is an invalid name")
        elif snapshot_name in self:
            syslog.warning("Snapshot already exists, data will be overwritten.")
            return self._snapshots[self._snapshot_metadata.index(snapshot_name)]
        else:
            new_snapshot = Snapshot(self.snapshot_dir / snapshot_name)
            self._snapshot_metadata.append(snapshot_name)
            self._snapshots.append(new_snapshot)
            new_snapshot.path.mkdir(mode=DIRMODE, parents=True, exist_ok=True)
            self.write_metadata(self._snapshot_metadata)

            syslog.debug("Snapshot created")
            syslog.debug(f"Snapshot name: {new_snapshot.name}")

            return new_snapshot

    def cleanup(self, *, remove_snapshots=False, remove_repo_dir=False):
        """Clean up any filesystem references to this repository.
        By default, no snapshots are deleted.

        :param remove_snapshots: delete the data directory of this repository
        :type remove_snapshots: bool
        :param remove_repo_dir: remove the top-directory level of this repository
        :type remove_repo_dir: bool
        """
        # We don't want to risk symlink attacks
        if not shutil.rmtree.avoids_symlink_attacks:
            syslog.error(
                "shutil cannot avoid symlink attacks on this platform. Ignoring."
            )
            return

        syslog.debug("Cleaning repository data")

        self.metadata_path.unlink()
        syslog.info("Removing repository metadata")
        syslog.debug(f"Repository metadata removed: {self.metadata_path}")

        if remove_snapshots:
            try:
                shutil.rmtree(self.snapshot_dir)
            except PermissionError as e:
                syslog.error(e)
            else:
                syslog.info("Removed snapshots")

        if remove_repo_dir:
            try:
                shutil.rmtree(self)
            except PermissionError as e:
                syslog.error(e)
            else:
                syslog.info(f"Removed repository directory: {self.path}")
