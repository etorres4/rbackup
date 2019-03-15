"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.repository
    :synopsis: Class for structuring a backup repository.
"""

import os.path
import datetime
import glob


class Repository(Hierarchy):
    """A class for interacting with a backup repository.

    At the time of creation, the following is true about the class:
    The current snapshot points to:
    -------------------------------
    * None if the repository is empty
    * The most recent snapshot before running create_snapshot()
    * A new, empty snapshot after running create_snapshot()

    The previous snapshot points to:
    --------------------------------
    * None if the repository is empty
    * The snapshot before the current snapshot if there is more than one
    * The 

    Attributes
    ----------
    * curr_snapshot - return either the most recent snapshot or
        the new snapshot created after running create_snapshot()
    * prev_snapshot - return the Snapshot of the previous backup
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

        self._snapshot_dir = os.path.join(self.base_path, "data")
        self.update_snapshots()
        self._prev_snapshot = None
        self._curr_snapshot = self._prev_snapshot

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

    def create_snapshot(self, name=datetime.datetime.utcnow().isoformat().replace(":", "-")):
        """
        :return: a new Snapshot object
        :rtype: Snapshot object
        """
        path = os.path.join(self._snapshot_dir, f"snapshot-{name}")

        self._curr_snapshot = Snapshot(path)
        self._snapshots.append(_curr_snapshot)

    def update_snapshots(self):
        """Update the list of snapshots in this repository."""
        self._snapshots = [
            Snapshot(s)
            for s in glob.glob(f"{self._snapshot_dir}/*")
            if os.path.isdir(s)
        ]

    @property
    def prev_snapshot(self):
        """Return the instance of the previous Snapshot.

        :rtype: Snapshot object
        """
        if self.snapshots is None:
            return None
        else:
            return self.snapshots[-1]

    @property
    def curr_snapshot(self):
        """Return this Repository's current snapshot.

        Example
        -------
        >>> repo = Repository('backup')
        >>> repo.curr_snapshot
        >>> Snapshot('backup/data/snapshot-{utcnow}')

        :rtype: Snapshot object
        """
        return self._curr_snapshot
