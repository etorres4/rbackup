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
    * boot_dir
    * etc_dir
    * home_dir
    * root_home_dir
    """

    def __init__(self, path):
        """Default constructor for the Snapshot class."""
        super().__init__(path)

    @property
    def boot_dir(self):
        """Retrieve the /boot backup directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-new')
        >>> s.boot_dir
        PosixPath('backup/data/snapshot-new/boot/loader')

        :rtype: path-like object
        """
        return self.path / "boot" / "loader"

    @property
    def etc_dir(self):
        """Retrieve the /etc backup directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-new')
        >>> s.etc_dir
        PosixPath('backup/data/snapshot-new/etc')

        :rtype: path-like object
        """
        return self.path / "etc"

    @property
    def home_dir(self):
        """Retrieve the /home backup directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-new')
        >>> s.home_dir
        PosixPath('backup/data/snapshot-new/home')

        :rtype: path-like object
        """
        return self.path / "home"

    @property
    def pkg_dir(self):
        """Retrieve the package manager backup directory of this snapshot.
        >>> s = Snapshot('backup/data/snapshot-new')
        >>> s.pkg_dir
        PosixPath('backup/data/snapshot-new/pkg')
        """
        return self.path / "pkg"

    @property
    def root_home_dir(self):
        """Retrieve root's home directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('backup/data/snapshot-new')
        >>> s.root_home_dir
        PosixPath('backup/data/snapshot-new/root')

        :rtype: path-like object
        """
        return self.path / "root"


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
