"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.struct.snapshot
    :synopsis: Class for creating the backup snapshot hierarchy.
"""
import logging

from rbackup.struct.hierarchy import Hierarchy

# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Classes ==========
class Snapshot(Hierarchy):
    """Hierarchy for a single snapshot.

    Data from each run of a backup script is intended to go here.

    Snapshots are unaware of one another, it is up to a third-party caller
    to orchestrate operations such as hardlinking between snapshots and
    ordering snapshots.
    """

    def __init__(self, path):
        """Default constructor for the Snapshot class."""
        super().__init__(path)

        self._pkg_dir = self.path / "pkg"

    def __repr__(self):
        """Return a string representation of this Snapshot."""
        return f"{self.__class__.__name__}('{self.name}')"

    @property
    def pkg_dir(self):
        """
        :returns: the package manager backup directory of this snapshot.
        :rtype: path-like object
        """
        return self._pkg_dir

    def gen_metadata(self):
        pass
