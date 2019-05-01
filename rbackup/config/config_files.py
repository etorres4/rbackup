"""
.. :author:: Eric Torres
.. :module:: rbackup.config.config_files
    :synopsis: Functions for handling config files.
"""
import configparser
import json
import logging
import re
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile

# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)

# ========== Constants ==========
COMMENT_REGEX = r"^[^#; ]+"

# ----- Paths -----
CONFIG_DIR = Path("/etc/rbackup")
MAIN_CONFIG_FILE = CONFIG_DIR / "backup.conf"

# ----- Exit Codes -----
E_NO_CONFIG_FILE = 4


# ========== Functions ==========
def get_files_by_suffix(suffix):
    """Retrieve all include files from the program configuration directory.

    >>> get_files_by_suffix('-include.conf') # doctest: +ELLIPSIS
    <generator object ...>

    :param suffix: the suffix to search for
    :type suffix: str
    :return: paths pointing to include files
    :rtype: generator of path-like objects
    """
    yield from CONFIG_DIR.glob(f"*{suffix}")


def load_list_from_option(parser, *, section="", option="", fallback=None):
    """Using a combination of ``ConfigParser`` and JSON, load a
    list from a configuration file option.

    :param parser: the parsed config file
    :type parser: ``ConfigParser`` object
    :param section: the section of the config file to load
    :type section: str
    :param option: the option value inside the specified section
    :type option: str
    :return: the list parsed by JSON
    :param fallback: the fallback value to return if the option is empty
    :type fallback: list
    :rtype: list
    """
    try:
        return json.loads(parser[section][option])
    except (json.decoder.JSONDecodeError, KeyError):
        return [] if fallback is None else fallback


def merge_files(files):
    """Parse, filter, and sort through config files to create a single
    --files-from argument.

    >>> merge_files(get_files_by_suffix('-include.conf')) # doctest: +ELLIPSIS
    PosixPath('/tmp/...')

    :param files: files including paths to read from
    :type files: iterable of path-like objects
    :return: path to file that lists include paths
    :rtype: path-like object
    """
    include_lines = []

    for file in files:
        with file.open(mode="r") as opened_file:
            include_lines.extend(
                l for l in opened_file.readlines() if re.match(COMMENT_REGEX, l)
            )

    include_lines.sort()

    with NamedTemporaryFile(mode="w", delete=False) as include_paths:
        include_paths.writelines(include_lines)

    return Path(include_paths.name)


@contextmanager
def merge_include_files():
    """Merge include file paths into one file and yield its path for use with rsync.

    :return: path-like object
    """
    try:
        filelist = merge_files(get_files_by_suffix("-include.conf"))
        yield filelist
    finally:
        filelist.unlink()


@contextmanager
def merge_exclude_files():
    """Merge exclude file paths into one file and yield its path for use with rsync.

    :return: path-like object
    """
    try:
        filelist = merge_files(get_files_by_suffix("-exclude.conf"))
        yield filelist
    finally:
        filelist.unlink()


def parse_configfile():
    """Parse the main backup config file and return
    a ``configparser.ConfigParser`` object.

    :return: object used to parse config file
    :rtype: ConfigParser object
    :raises FileNotFoundError: if path does not exist
    """
    if not MAIN_CONFIG_FILE.is_file():
        raise FileNotFoundError(f"{MAIN_CONFIG_FILE} does not exist")

    config_reader = configparser.ConfigParser()
    config_reader.read(MAIN_CONFIG_FILE)

    return config_reader
