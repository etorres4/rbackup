"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.struct.snapshot
    :synopsis: Class for creating the backup snapshot hierarchy.
"""
import datetime
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

        self._gen_metadata()

        self._pkg_dir = self.path / "pkg"

    def __dir__(self):
<<<<<<< HEAD
        return [super().__dir__(), "ctime", "pkg_dir"]
=======
        return super().__dir__(), "ctime", "pkg_dir"
>>>>>>> 2aff6704bc8f14d9a3f73178c4c1709bfc7812b5

    def __repr__(self):
        """Return a string representation of this Snapshot."""
        return f"{self.__class__.__name__}('{self.name}')"

    def _gen_metadata(self):
        """Generate this Snapshot's metadata."""
        if self.metadata_path.exists():
            self._ctime = self.read_metadata()
        else:
            self._ctime = datetime.datetime.utcnow().isoformat()
            self.write_metadata(self._ctime)

    @property
    def ctime(self):
        """
        :returns: this Snapshot's creation time
        :rtype: str
        """
        return self._ctime

    @property
    def pkg_dir(self):
        """
        :returns: the package manager backup directory of this snapshot.
        :rtype: path-like object
        """
        return self._pkg_dir
