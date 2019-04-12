"""
.. author:: Eric Torres
.. module:: rbackup.struct.hierarchy
:synopsis: Classes for creating the backup hierarchy.
"""
import json
import logging
from os import PathLike
from pathlib import Path

# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Constants ==========
METADATA_READ = "r"
METADATA_WRITE = "w"


# ========== Classes ==========
class Hierarchy(PathLike):
    """A class for organizing the backup root hierarchy.

    Upon creation of a Hierarchy object, it is up to the caller
    to call either shutil.mkdir() or a related method to create
    the directory structure it emulates.

    For consistency, Hierarchy objects always store and return absolute paths.

    Attributes
    ----------
    * Hierarchy.path
    * Hierarchy.name
    * Hierarchy.metadata_path

    Methods
    -------
    * gen_metadata - generate the metadata for this Hierarchy
    * read_metadata - read this Hierarchy's metadata from a file
        and return it
    * write_metadata - write this Hierarchy's metadata to a file
    """

    def __init__(self, dest):
        """Default constructor for the Hierarchy class.

        >>> Hierarchy('backup_dir').path
        PosixPath('backup_dir')

        :param dest: the root directory of the backup hierarchy
        :type dest: str or path-like object
        """
        try:
            self._path = Path(dest).resolve()
        except TypeError as e:
            raise e

    def __fspath__(self):
        return str(self._path)

    def __repr__(self):
        """Return a string representation of this Hierarchy."""
        return f"{self.__class__.__name__}('{self._path}')"

    @property
    def path(self):
        """Return the base directory of this hierarchy.

        >>> Hierarchy('backup').path
        PosixPath('backup')

        :rtype: path-like object
        """
        return self._path

    @property
    def name(self):
        """Return the name of this hierarchy.

        >>> Hierarchy('backup/data/snapshot-one').name
        'snapshot-one'

        :rtype: str
        """
        return self._path.name

    @property
    def metadata_path(self):
        """Return the path of this hierarchy's metadata file.

        >>> Hierarchy('backup').metadata_path
        PosixPath('backup/.metadata')

        :rtype: path-like object
        """
        return self._path / ".metadata"

    def gen_metadata(self):
        """Generate metadata for this repository.
            After this method is called, the data necessary for this repository has been created.
        """
        raise NotImplementedError("This method must be called in a child class.")

    def read_metadata(self):
        """Read this repository's metadata from its file and
        then return it.

        :rtype: type that the data is serialized as
        """
        syslog.debug(f"Reading metadata from {self.metadata_path}")
        with self.metadata_path.open(mode=METADATA_READ) as mfile:
            return json.load(mfile)

    def write_metadata(self, attr):
        """Write this repository's metadata to its file.
            Note that this write operation is atomic to the caller.

        :param attr: data to write to file
        :type attr: class member to write
        """
        syslog.debug(f"Writing metadata to {self.metadata_path}")

        tmpfile = self.metadata_path.with_suffix(".tmp")

        with tmpfile.open(mode=METADATA_WRITE) as mfile:
            json.dump(attr, mfile)

        tmpfile.rename(self.metadata_path)
