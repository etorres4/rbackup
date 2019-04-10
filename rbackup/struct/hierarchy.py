"""
.. author:: Eric Torres
.. module:: rbackup.struct.hierarchy
    :synopsis: Classes for creating the backup hierarchy.
"""
import logging
import pickle

from os import PathLike
from pathlib import Path

# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Constants ==========
METADATA_READ = "rb"
METADATA_WRITE = "wb"


# ========== Classes ==========
class Hierarchy(PathLike):
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
        :type dest: str or path-like object
        """
        try:
            self._path = Path(dest)
        except TypeError as e:
            raise e

    def __repr__(self):
        """Return a string representation of this Hierarchy."""
        return f"{self.__class__.__name__}('{self._path}')"

    def __fspath__(self):
        return str(self._path)

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
        return self._path.name

    @property
    def metadata_path(self):
        """Return the path of this hierarchy's metadata file.

        >>> hier = Hierarchy('backup')
        >>> hier.metadata_path
        PosixPath('backup/.metadata')

        :rtype: path-like object
        """
        return self._path / ".metadata"

    def read_metadata(self):
        """Read this repository's metadata from its file and
        then return it.

        :rtype: dict
        """
        syslog.debug(f"Reading metadata from {self.metadata_path}")
        with self.metadata_path.open(mode=METADATA_READ) as mfile:
            return pickle.load(mfile)

    def write_metadata(self):
        """Write this repository's metadata to its file.
            Note that this write operation is atomic to the caller.
        """
        syslog.debug(f"Writing metadata to {self.metadata_path}")

        tmpfile = self.metadata_path.with_suffix(".tmp")

        with tmpfile.open(mode=METADATA_WRITE) as mfile:
            pickle.dump(self._data, mfile)

        tmpfile.rename(self.metadata_path)


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
