"""This module contains a class for creating a backup hierarchy."""
import os.path

class Hierarchy():
    dest = None

    def Hierarchy(self, dest):
        """Default constructor for the hierarchy class.

        :param dest: the root directory of the backup hierarchy
        :type dest: str, bytes, or path-like object
        """
        if not os.path.isdir(dest):
            raise ValueError(f"{dest} is not a valid directory")

        self.dest = dest

    @property
    def etc_dir: 
        """Retrieve the /etc backup directory of this hierarchy.

        :rtype: str
        """
        return os.path.join(self.dest, backup, etc)

    @property
    def home_dir:
        """Retrieve the /home backup directory of this hierarchy.

        :rtype: str
        """
        return os.path.join(self.dest, backup, home)

    @property
    def snapshot_dir:
        """Retrieve the snapshot directory of this hierarchy.

        :rtype: str
        """
        return os.path.join(self.dest, backup, snapshots)

    @property
    def root_home_dir:
        """Retrieve root's home directory of this hierarchy.

        :rtype: str
        """
        return os.path.join(self.dest, backup, root)

    @property
    def base_dir:
        """Return the base directory of this hierarchy.

        :rtype: str
        """
        return dest
