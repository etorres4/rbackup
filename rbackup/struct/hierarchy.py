"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.struct.hierarchy
    :synopsis: Classes for creating the backup hierarchy.
"""
import json
import logging
import shutil
from os import PathLike
from pathlib import Path

# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Constants ==========
DIRMODE = 0o755
FILEMODE = 0o644

METADATA_READ = "r"
METADATA_WRITE = "w"


# ========== Classes ==========
class Hierarchy(PathLike):
    """A general class for organizing a hierarchy of data.

    **Implementation Details**

    * For consistency, ``Hierarchy`` objects always store and return absolute paths
    * Data for all ``Hierarchy`` objects and subclassed objects use JSON for serialization
    * ``Hierarchy`` objects create their directories upon instantiation
      * This may result in a ``PermissionError``
    """

    def __init__(self, dest):
        """Default constructor for the Hierarchy class.

        :param dest: the root directory of the backup hierarchy
        :type dest: str or path-like object
        :raises PermissionError: if process does not have permission to write at dest
        """
        self._path = Path(dest).resolve()
        self._metadata_path = self._path / ".metadata"
        self._name = self._path.name

        self.path.mkdir(DIRMODE, parents=True, exist_ok=True)

    def __eq__(self, other):
        return self._path == other.path

    def __fspath__(self):
        return str(self._path)

    def __hash__(self):
        return hash(self._path)

    def __ne__(self, other):
        return self._path != other.path

    def __repr__(self):
        """Return a string representation of this Hierarchy."""
        return f"{self.__class__.__name__}('{self._path}')"

    def __str__(self):
        """Return a string representation of this Hierarchy."""
        return str(self._path)

    def __dir__(self):
<<<<<<< HEAD
        return [
=======
        return (
>>>>>>> 2aff6704bc8f14d9a3f73178c4c1709bfc7812b5
            "__dir__",
            "__eq__",
            "__fspath__",
            "__hash__",
            "__ne__",
            "__repr__",
            "__str__",
            "path",
            "name",
            "metadata_path",
            "cleanup",
            "read_metadata",
            "write_metadata",
<<<<<<< HEAD
        ]
=======
        )
>>>>>>> 2aff6704bc8f14d9a3f73178c4c1709bfc7812b5

    def _gen_metadata(self):
        """Generate metadata for this repository.

            After this method is called, the data necessary for this hierarchy has been created.
        """
        raise NotImplementedError("This method must be called in a child class.")

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

    def cleanup(self, **kwargs):
        """Clean up this Hierarchy's data from the filesystem."""

        syslog.info(f"Performing cleanup on {self._path}")

        # We don't want to risk symlink attacks
        # noinspection PyUnresolvedReferences
        if not shutil.rmtree.avoids_symlink_attacks:
            syslog.error(
                "shutil cannot avoid symlink attacks on this platform. Ignoring."
            )
            return

        shutil.rmtree(self)

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
