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
    * Snapshot.path (inherited from Hierarchy)
    * Snapshot.name (inherited from Hierarchy)
    * Snapshot.metadata_path (inherited from Hierarchy)
    * Snapshot.pkg_dir

    Methods
    -------
    * gen_metadata (inherited from Hierarchy)
    * read_metadata (inherited from Hierarchy)
    * write_metadata (inherited from Hierarchy)
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
        """Retrieve the package manager backup directory of this snapshot.

        :rtype: path-like object
        """
        return self._pkg_dir

    def gen_metadata(self):
        """Generate metadata for this repository.
            After this method is called, the data necessary for this snapshot has been created.
        """
        pass


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
