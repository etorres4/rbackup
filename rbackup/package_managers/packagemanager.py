"""
.. author:: Eric Torres
.. module:: rbackup.packagemanager
:synopsis: Module for package manager plugins
"""
import logging
import subprocess
import tarfile

from collections.abc import Iterable
from pathlib import Path
from tempfile import NamedTemporaryFile

# ========== Constants ==========


# ========== Logging Setup ==========
syslog = logging.getLogger(__name__)


# ========== Classes ==========
class PackageManager:
    def __init__(self, cachedir, db_path, pkglist_cmd):
        """Default constructor for the PackageManager class.

        :param cachedir: path to the package manager cache directory
        :type cachedir: str or path-like object
        :param db_path: path to the package manager database
        :type db_path: str or path-like object
        :param pkglist_cmd: command to list installed packages to stdout
        :type pkglist_cmd: list
        """
        if not isinstance(pkglist_cmd, Iterable) or isinstance(pkglist_cmd, dict):
            raise TypeError("pkglist_cmd is the wrong type")
        elif not pkglist_cmd:
            raise ValueError(f"Package list command is empty: {pkglist_cmd}")
        elif any(not isinstance(arg, str) for arg in pkglist_cmd):
            raise TypeError(f"{pkglist_cmd} contains a non-str value")
        elif any(not bool(arg) for arg in pkglist_cmd):
            raise ValueError(f"{pkglist_cmd} contains an empty str value")

        self._cachedir = Path(cachedir)
        self._db_path = Path(db_path)
        self._pkglist_cmd = pkglist_cmd

    def __init_subclass__(cls, cachedir, db_path, pkglist_cmd):
        """Default constructor for all child classes."""
        super().__init_subclass(cachedir, db_path, pkglist_cmd)

    def _gen_pkglist(self):
        """Generate a text file listing installed packages
        on the system and return the path to that file.

            If there is an error in the package listing command, then
            it is to be assumed that no file was created, therefore there
            is no file to cleanup.

            Note that this method is internal and is
            meant to be called from a subclass in a separate module.

        :returns: path to temporary file
        :rtype: path-like object
        """
        syslog.info("Creating a package list")

        try:
            process = subprocess.run(self._pkglist_cmd, capture_output=True)
        except subprocess.CalledProcessError as e:
            syslog.error(e)
        else:
            with NamedTemporaryFile(mode="wb", delete=False) as pkglist:
                pkglist.write(process.stdout)

            syslog.info("Package list generation complete")
            return Path(pkglist.name)

    def _gen_db_archive(self, *args, **kwargs):
        """Generate a database archive for this package manager.

            Note that this method is internal and is
            meant to be called from a subclass in a separate module.

            All arguments and keyword-only arguments are passed directly
            to the packagemanagerk

        :returns: the path to the created file
        :rtype: path-like object
        """
        raise NotImplementedError

        syslog.info("Creating a database archive")

        with NamedTemporaryFile(delete=False) as db_archive:
            archive = tarfile.open(*args, **kwargs)

            archive.add(cachedir)

        syslog.info("Database archive generation complete")

        return Path(db_archive.name)

    @property
    def cache_directory(self):
        """Return the cache directory of this package manager.
        
        :rtype: path-like object
        """
        return self._cachedir

    @property
    def database_path(self):
        """Return the database path of this package manager.

        :rtype: path-like object
        """
        return self._db_path

    @property
    def pkglist_cmd(self):
        """Return the package listing command of this package manager.
        
        :rtype: iterable or str
        """
        return self._pkglist_cmd


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
