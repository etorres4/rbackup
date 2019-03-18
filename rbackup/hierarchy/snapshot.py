"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.snapshot
    :synopsis: Classes for creating the /tmp hierarchy.
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

        self._boot_dir = self.path / "boot"
        self._etc_dir = self.path / "etc"
        self._home_dir = self.path / "home"
        self._root_home_dir = self.path / "root"

    @property
    def boot_dir(self):
        """Retrieve the /boot /tmp directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('/tmp/data/snapshot-new')
        >>> s.boot_dir
        PosixPath('/tmp/data/snapshot-new/boot')

        :rtype: path-like object
        """
        return self._boot_dir

    @property
    def etc_dir(self):
        """Retrieve the /etc /tmp directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('/tmp/data/snapshot-new')
        >>> s.etc_dir
        PosixPath('/tmp/data/snapshot-new/etc')

        :rtype: path-like object
        """
        return self._etc_dir

    @property
    def home_dir(self):
        """Retrieve the /home /tmp directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('/tmp/data/snapshot-new')
        >>> s.home_dir
        PosixPath('/tmp/data/snapshot-new/home')

        :rtype: path-like object
        """
        return self._home_dir

    @property
    def root_home_dir(self):
        """Retrieve root's home directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('/tmp/data/snapshot-new')
        >>> s.root_home_dir
        PosixPath('/tmp/data/snapshot-new/root')

        :rtype: path-like object
        """
        return self._root_home_dir


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
