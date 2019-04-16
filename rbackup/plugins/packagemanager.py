"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.plugins.packagemanager
    :synopsis: Module for package manager plugins.
"""
import logging
import subprocess
import tarfile

from pathlib import Path
from tempfile import NamedTemporaryFile

# ========== Constants ==========
LOCKFILE_MODE = 0o0000
VALID_DB_COMPRESS_MODES = [None, "bzip2", "gz", "lzma", "xz"]

# ========== Logging Setup ==========
syslog = logging.getLogger(__name__)


# ========== Classes ==========
class PackageManager:
    """Class for abstracting package manager-based operations.

    The package manager can be used in conjunction with a ``Snapshot`` for backups.

    Lockfile Management
    ^^^^^^^^^^^^^^^^^^^

    This class can be used as a context manager for creating a lockfile for the
    specific package manager. This is to prevent transactions from occurring during
    backup operations which would most likely leave the package manager's database in
    an inconsistent state on the backup.

        .. note:: Subclasses can override the context manager and implement i.e. blocking until
            the process is complete with a timeout.
    """

    def __init__(self, cachedir=None, db_path=None, lockfile=None, pkglist_cmd=None):
        """Default constructor for the PackageManager class.

        :param cachedir: path to the package manager cache directory
        :type cachedir: str or path-like object
        :param db_path: path to the package manager database
        :type db_path: str or path-like object
        :param lockfile: path to this package manager's lockfile
        :type lockfile: str
        :param pkglist_cmd: command to list installed packages to stdout
        :type pkglist_cmd: str or iterable of str
        """
        self._cachedir = Path(cachedir)
        self._db_path = Path(db_path)
        self._lockfile = Path(lockfile)
        self._pkglist_cmd = pkglist_cmd

    def __enter__(self):
        """Create the package manager's lockfile. This prevents transactions
        from occurring during the backup which could leave the database backup
        in an inconsistent state.

            The existence of this lockfile is an error, and its meaning is up to
            the package manager. For example, pacman's db.lck indicates
            either there is an ongoing transaction in progress or a previous transaction
            failed and the database is in an inconsistent state.

        :returns: self
        :rtype: ``PackageManager`` object
        :raises FileExistsError: if lockfile exists when this method is called
        """
        self._lockfile.touch(mode=0o000)
        yield self

    def __exit__(self):
        """Remove the package manager's lockfile. After this lockfile is closed,
        the package manager this class abstracts can perform transactions once again.
        """
        self._lockfile.unlink()

    def gen_pkglist(self):
        """Generate a text file listing installed packages
        on the system and return the path to that file.

            If there is an error in the package listing command, then
            it is to be assumed that no file was created, therefore there
            is no file to cleanup.

        :returns: path to temporary file
        :rtype: path-like object
        :raises NotImplementedError: if package list generation command is not present
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

    def gen_db_archive(self, compress=None):
        """Generate a database archive for this package manager.

            All arguments and keyword-only arguments are passed directly
            to the PackageManager object.

        :param compress: compression mode
        :type compress: str
        :returns: the path to the created file
        :rtype: path-like object
        :raises ValueError: if compress is not in packagemanager.VALID_DB_COMPRESS_MODES
        :raises NotImplementedError: if database path is not present
        """
        if compress is not None and compress not in VALID_DB_COMPRESS_MODES:
            raise ValueError(f"{compress} is not a valid compress mode")

        syslog.info("Creating a database archive")

        archivemode = "w" if compress is None else f"w:{compress}"
        archivesuffix = ".tar" if compress is None else f".tar.{compress}"

        with NamedTemporaryFile(delete=False, suffix=archivesuffix) as tmpfile:
            archive_path = Path(tmpfile.name)

        with tarfile.open(name=archive_path, mode=archivemode) as db_archive:
            db_archive.add(self.database_path)

        syslog.info("Database archive generation complete")

        return archive_path

    @property
    def cache_directory(self):
        """
        :returns: the cache directory of this package manager
        :rtype: path-like object
        """
        return self._cachedir

    @property
    def database_path(self):
        """
        :returns: the database path of this package manager
        :rtype: path-like object
        """
        return self._db_path

    @property
    def lockfile(self):
        """
        :returns: the lockfile path of this package manager
        :rtype: path-like object
        """
        return self._lockfile

    @property
    def pkglist_cmd(self):
        """
        :returns: the package listing command of this package manager
        :rtype: iterable or str
        """
        return self._pkglist_cmd
