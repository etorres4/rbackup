"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.hierarchy
    :synopsis: Classes for creating the backup hierarchy.
"""
import logging

from pathlib import Path

# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Classes ==========
class Hierarchy:
    """A class for organizing the backup root hierarchy.

    Upon creation of a Hierarchy object, it is up to the caller
    to call either shutil.mkdir() or a related method to create
    the directory structure it emulates.

    Attributes
    ----------
    * path
    * name
    """

    def __init__(self, dest):
        """Default constructor for the Hierarchy class.

        Example
        -------
        >>> hier = Hierarchy('backup')
        >>> hier.path
        PosixPath('backup')

        :param dest: the root directory of the backup hierarchy
        :type dest: str, path-like object
        """
        try:
            self._path = Path(dest)
        except TypeError as e:
            raise e

        self._metadata_path = self.path / ".metadata"

    @property
    def path(self):
        """Return the base directory of this hierarchy.

        Example
        -------
        >>> hier = Hierarchy('backup')
        >>> hier.path
        PosixPath('backup')

        :rtype: path-like object
        """
        return self._path

    @property
    def name(self):
        """Return the name of this hierarchy.

        Example
        -------
        >>> hier = Hierarchy('backup/data/snapshot-one')
        >>> hier.name
        'snapshot-one'

        :rtype: str
        """
        return self.path.name


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
