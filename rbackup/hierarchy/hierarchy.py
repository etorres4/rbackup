"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy
    :synopsis: Classes for creating the backup hierarchy.
"""

import os.path
import datetime
import glob


class Hierarchy:
    """A class for organizing the backup root hierarchy.
    See README.rst for more details."""

    def __init__(self, dest):
        """Default constructor for the Hierarchy class.

        :param dest: the root directory of the backup hierarchy
        :type dest: str, bytes
        :raises: NotADirectoryError if dest is not a directory
        """
        if not os.path.isdir(dest):
            raise NotADirectoryError(f"{dest}: no such directory")

        self.dest = dest

    @property
    def base_path(self):
        """Return the base directory of this hierarchy.

        >>> h = Hierarchy('backup')
        >>> h.base_path
        >>> 'backup'

        :rtype: str
        """
        return self.dest
