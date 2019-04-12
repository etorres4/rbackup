"""
.. author:: Eric Torres
.. module:: rbackup.struct.snapshot
    :synopsis: Classes for creating the backup hierarchy.
"""
import logging

from rbackup.struct.hierarchy import Hierarchy

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
    * gen_metadata (inherited from Hierarchy)
    * read_metadata (inherited from Hierarchy)
    * write_metadata (inherited from Hierarchy)
    """

    def __init__(self, path):
        """Default constructor for the Snapshot class."""
        super().__init__(path)

    def __repr__(self):
        """Return a string representation of this Snapshot."""
        return f"{self.__class__.__name__}('{self.name}')"

    @property
    def pkg_dir(self):
        """Retrieve the package manager backup directory of this snapshot.

        :rtype: path-like object
        """
        return self.path / "pkg"


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
