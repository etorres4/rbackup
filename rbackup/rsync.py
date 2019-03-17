"""
.. author:: Eric Torres
.. module:: rbackup.rsync
    :synopsis: helper functions for running the rsync backend
"""
import logging
import subprocess


# ========== Constants ==========
_RSYNC_BIN = "/usr/bin/rsync"


# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)

# ========== Functions ==========
def rsync(*args):
    """Run an rsync command.

    :param args: all arguments to pass to rsync
    :type args: str
    :raises: subprocess.CalledProcessError if rsync process failed
    """
    cmd = [_RSYNC_BIN, *args]

    syslog.debug(f"rsync command: {cmd}")
    syslog.info("Beginning rsync process")

    try:
        process = subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        raise e

    syslog.debug(process.stdout)
    syslog.info("Process complete")
