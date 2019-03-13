"""This module contains a class for creating a backup hierarchy."""

import os.path
import datetime


class Hierarchy:
    """A class for generating the backup root hierarchy.
    """

    def __init__(self, dest):
        """Default constructor for the hierarchy class.

        :param dest: the root directory of the backup hierarchy
        :type dest: str, bytes, or path-like object
        """
        if not os.path.isdir(dest):
            raise ValueError(f"{dest} is not a valid directory")

        self.dest = dest

    @property
    def base_dir(self):
        """Return the base directory of this hierarchy.

        :rtype: str
        """
        return self.dest

    @property
    def prev_snapshot(self):
        """Return the canonical path of the previous snapshot stored in
        this hierarchy.

        This method checks whether or not '/dest/prev' is a symlink to
        a snapshot. If it is not, then a FileExistsError is raised.

        :rtype: str
        :raises: FileExistsError if 'dest/prev' is not a symlink
            to a snapshot
        """
        prevpath = os.path.join(self.base_dir, "prev")

        if os.path.exists(prevpath) and not os.path.islink(prevpath):
            raise FileExistsError(f"{prevpath} exists and is not a symlink")
        elif not os.path.exists(prevpath):
            raise FileNotFoundError(f"prevpath does not exist")

        return os.path.realpath(prevpath)

    @property
    def prev_snapshot_link(self):
        """Return the symlink path of the previous snapshot stored in
        this hierarchy.

        :rtype: str
        """
        return os.path.join(self.base_dir, "prev")

    @property
    def curr_snapshot(self):
        """Retrieve the current date and time and use that in the path
        for the current snapshot-to-be.

        :rtype: str
        """
        date = datetime.datetime.utcnow().isoformat()
        return os.path.join(self.base_dir, date.replace(":", "-"))

    @property
    def etc_dir(self):
        """Retrieve the /etc backup directory of this hierarchy.

        :rtype: str
        """
        return os.path.join(self.curr_snapshot, "etc")

    @property
    def home_dir(self):
        """Retrieve the /home backup directory of this hierarchy.

        :rtype: str
        """
        return os.path.join(self.curr_snapshot, "home")

    @property
    def snapshot_dir(self):
        """Retrieve the snapshot directory of this hierarchy.

        :rtype: str
        """
        return os.path.join(self.curr_snapshot, "snapshots")

    @property
    def root_home_dir(self):
        """Retrieve root's home directory of this hierarchy.

        :rtype: str
        """
        return os.path.join(self.curr_snapshot, "root")
