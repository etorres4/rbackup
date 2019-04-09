"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.snapshot
    :synopsis: Classes for creating the backup hierarchy.
"""
import logging

from rbackup.hierarchy.hierarchy import Hierarchy


# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Classes ==========
class Snapshot(Hierarchy):
    """Hierarchy for a single snapshot.
    Attributes
    ----------
    * path (inherited from Hierarchy)
    * name (inherited from Hierarchy)
    * metadata_path (inherited from Hierarchy)
    * pkg_dir

    Methods
    -------
    * read_metadata (inherited from Hierarchy)
    * write_metadata (inherited from Hierarchy)
    """

    def __init__(self, path):
        """Default constructor for the Snapshot class."""
        super().__init__(path)

    @property
    def pkg_dir(self):
        """Retrieve the package manager backup directory of this snapshot.
        >>> s = Snapshot('backup/data/snapshot-new')
        >>> s.pkg_dir
        PosixPath('backup/data/snapshot-new/pkg')

        :rtype: path-like object
        """
        return self.path / "pkg"


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
