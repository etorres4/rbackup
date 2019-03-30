"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.hierarchy
    :synopsis: Classes for creating the backup hierarchy.
"""
import logging
import pickle

from pathlib import Path

# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Constants ==========
METADATA_READ = "rb"
METADATA_WRITE = "wb"


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
    * metadata_path

    Methods
    -------
    * read_metadata - read this Hierarchy's metadata from a file
        and return it
    * write_metadata - write this Hierarchy's metadata to a file
    """

    def __init__(self, dest):
        """Default constructor for the Hierarchy class.

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

    @property
    def path(self):
        """Return the base directory of this hierarchy.

        >>> hier = Hierarchy('backup')
        >>> hier.path
        PosixPath('backup')

        :rtype: path-like object
        """
        return self._path

    @property
    def name(self):
        """Return the name of this hierarchy.

        >>> hier = Hierarchy('backup/data/snapshot-one')
        >>> hier.name
        'snapshot-one'

        :rtype: str
        """
        return self.path.name

    @property
    def metadata_path(self):
        """Return the path of this hierarchy's metadata file.

        >>> hier = Hierarchy('backup')
        >>> hier.metadata_path
        PosixPath('backup/.metadata')

        :rtype: path-like object
        """
        return self.path / ".metadata"

    def read_metadata(self):
        """Read this repository's metadata from its file and
        then return it.

        :rtype: dict
        """
        with self.metadata_path.open(mode=METADATA_READ) as mfile:
            return pickle.load(mfile)

    def write_metadata(self):
        """Write this repository's metadata to its file."""
        with self.metadata_path.open(mode=METADATA_WRITE) as mfile:
            pickle.dump(self._data, mfile)


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
