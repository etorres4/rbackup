"""
.. author:: Eric Torres
.. module:: r/tmp.hierarchy.snapshot
    :synopsis: Classes for creating the /tmp hierarchy.
"""
import os.path

from rbackup.hierarchy.hierarchy import Hierarchy


class Snapshot(Hierarchy):
    """Hierarchy for a single snapshot.
    Attributes
    ----------
    * path (inherited from Hierarchy)
    * name
    * boot_dir
    * etc_dir
    * home_dir
    * root_home_dir
    """

    def __init__(self, path):
        """Default constructor for the Snapshot class."""
        super().__init__(path)

    @property
    def name(self):
        """Return the name of this snapshot.

        Example
        -------
        >>> s = Snapshot('/tmp/data/snapshot-new')
        >>> s.name
        'snapshot-new'

        :rtype: str
        """
        return os.path.basename(self.path)

    @property
    def boot_dir(self):
        """Retrieve the /boot /tmp directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('/tmp/data/snapshot-new')
        >>> s.boot_dir
        '/tmp/data/snapshot-new/boot'

        :rtype: str
        """
        return os.path.join(self.path, "boot")

    @property
    def etc_dir(self):
        """Retrieve the /etc /tmp directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('/tmp/data/snapshot-new')
        >>> s.etc_dir
        '/tmp/data/snapshot-new/etc'

        :rtype: str
        """
        return os.path.join(self.path, "etc")

    @property
    def home_dir(self):
        """Retrieve the /home /tmp directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('/tmp/data/snapshot-new')
        >>> s.home_dir
        '/tmp/data/snapshot-new/home'

        :rtype: str
        """
        return os.path.join(self.path, "home")

    @property
    def root_home_dir(self):
        """Retrieve root's home directory of this snapshot.

        Example
        -------
        >>> s = Snapshot('/tmp/data/snapshot-new')
        >>> s.root_home_dir
        '/tmp/data/snapshot-new/root'

        :rtype: str
        """
        return os.path.join(self.path, "root")


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
