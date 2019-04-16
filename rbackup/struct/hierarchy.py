"""
.. moduleauthor:: Eric Torres
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
    """A general class for organizing a hierarchy of data.

    Hierarchy objects are non-intrusive in that they do not affect
    the filesystem upon creation. It is up to the caller
    to call either :func:`shutil.mkdir` or related method to create
    the directory structure it emulates.

    **Implementation Details**

    * For consistency, ``Hierarchy`` objects always store and return absolute paths
    * Data for all ``Hierarchy`` objects and subclassed objects use JSON for serialization
    """

    def __init__(self, dest):
        """Default constructor for the Hierarchy class.

        :param dest: the root directory of the backup hierarchy
        :type dest: str or path-like object
        """
        self._path = Path(dest).resolve()
        self._metadata_path = self._path / ".metadata"
        self._name = self._path.name

    def __fspath__(self):
        return str(self._path)

    def __repr__(self):
        """Return a string representation of this Hierarchy."""
        return f"{self.__class__.__name__}('{self._path}')"

    @property
    def path(self):
        """
        :returns: the base directory of this hierarchy
        :rtype: path-like object
        """
        return self._path

    @property
    def name(self):
        """
        :returns: the name of this hierarchy.
        :rtype: str
        """
        return self._name

    @property
    def metadata_path(self):
        """
        :returns: the path of this hierarchy's metadata file.
        :rtype: path-like object
        """
        return self._metadata_path

    def gen_metadata(self):
        """Generate metadata for this repository.

            After this method is called, the data necessary for this hierarchy has been created.
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
        """Write this repository's metadata to its metadata file.

        .. note:: This write operation is atomic to the caller.

        :param attr: class data to write to file
        :type attr: any type
        """
        syslog.debug(f"Writing metadata to {self.metadata_path}")

        tmpfile = self.metadata_path.with_suffix(".tmp")

        with tmpfile.open(mode=METADATA_WRITE) as mfile:
            json.dump(attr, mfile)

        tmpfile.rename(self.metadata_path)
