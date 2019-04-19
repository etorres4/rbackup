"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.rsync
    :synopsis: helper functions for running the rsync backend
"""
import logging
import subprocess


# ========== Constants ==========
_RSYNC_BIN = "/usr/bin/rsync"
DEFAULT_RSYNC_OPTS = [
    "--acls",
    "--archive",
    "--hard-links",
    "--ignore-missing-args",
    "--prune-empty-dirs",
    "--recursive",
    "--xattrs",
]


# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Functions ==========
def rsync(*args):
    """Run an rsync command.

    :param args: all arguments to pass to rsync including source and destination
    :type args: str
    :raises subprocess.CalledProcessError: if rsync process failed
    """
    cmd = [_RSYNC_BIN, *args]

    syslog.debug(f"rsync command: {cmd}")
    syslog.info("Beginning rsync process")

    process = subprocess.run(cmd, capture_output=True, check=True, text=True)

    syslog.debug(process.stdout)
    syslog.info("Process complete")
