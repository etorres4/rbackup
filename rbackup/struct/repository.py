"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.struct.repository
    :synopsis: Classes for structuring a backup repository.
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

    Properties

    * Each snapshot in a repository is unaware of one another,
      this is the job of the repository to organize
    * The only way snapshots are linked together is in files
      that are hard-linked together

    Snapshots can be accessed on a one-by-one basis through iteration.

    ::

        >>> for snapshot in Repository('backup'):
        >>>     print(snapshot.path)
        first
        second
        ...

    Snapshots on repositories can be retrieved by index using python's
    list slicing syntax.

    ::

        >>> print(Repository('backup')[:])
        [Snapshot(...), ...]

    Membership of a snapshot in a repository can be checked by name.

    ::

        >>> Repository('backup').create_snapshot('test')
        >>> 'test' in Repository('backup')
        True

    Number of snapshots in a repository can be checked as well

    ::

        >>> Repository('backup').create_snapshot()
        >>> len(Repository('backup'))
        1
    """
    """Snapshots are serialized as their names relative to the repository
    data directory, but have their full paths during runtime.

    Private Attributes
    * _snapshots - list of Snapshot objects created and accessed at runtime
    * _snapshot_metadata - list of Snapshot names serialized and deserialized
        when this Repository is first created
    """

    def __init__(self, dest):
        """Default constructor for the Repository class."""
        super().__init__(dest)

        if self.metadata_path.exists():
            self._snapshot_metadata = self.read_metadata()
        else:
            self.gen_metadata()

        self._snapshots = [
            Snapshot(self.snapshot_dir / s) for s in self._snapshot_metadata
        ]

        self._snapshot_iterator = iter(self._snapshots)

    def __contains__(self, name):
        """Check membership of a Snapshot in this Repository by name.

        :returns: True if name is the name of a Snapshot in this Repository
        :type name: str
        :rtype: bool
        """
        return name in self._snapshot_metadata

    def __delitem__(self, s):
        """Delete a Snapshot in this Repository."""
        raise NotImplementedError

    def __getitem__(self, idx):
        """Retrieve a Snapshot at a certain index."""
        return self._snapshots[idx]

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

        * Contain slashes
        * Are empty values

        Valid names:

        * Match the regex r'[\\w]+[^/]*'

        :param name: name to validate
        :type name: str
        :returns: true if this name is deemed valid, otherwise False
        :rtype: bool
        """
        return bool(re.match(VALID_SNAPSHOT_NAME, name))

    @property
    def snapshot_dir(self):
        """
        :returns: the directory in this Repository in which snapshots
            are stored.
        :rtype: path-like object
        """
        return self.path / "data"

    @property
    def snapshots(self):
        """
        :returns: all snapshots stored in this repository
        :rtype: list of Snapshot objects
        """
        return self._snapshots

    @property
    def empty(self):
        """
        :returns: True if there are no Snapshots in this Repository,
            False otherwise
        :rtype: bool
        """
        return not self.snapshots

    def gen_metadata(self):
        """Generate metadata for this repository.
            After this method is called, the data necessary for this snapshot has been created.
        """
        self._snapshot_metadata = []
        self.metadata_path.parent.mkdir(mode=DIRMODE, exist_ok=True)
        self.metadata_path.touch(mode=FILEMODE)
        self.write_metadata(self._snapshot_metadata)

    def create_snapshot(self, name=None):
        """Create a new snapshot in this repository.

        This operation is non-intrusive in that it will not
        make any changes in the filesystem when called.

        If name is not given, then the new snapshot's name is the current
        UTC date in ISO format.

        If name is given, then it is the name for the new snapshot.

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
        :param remove_repo_dir: remove the top-level directory of this repository
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
