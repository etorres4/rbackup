"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.system
    :synopsis: library for interacting with rbackup over the network
"""

import logging
import os
from contextlib import contextmanager

# ========== Constants ==========
DEFAULT_UMASK = 0000


# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Functions ==========
@contextmanager
def change_umask(override=None):
    """Creates a context manager in which the umask is changed.
    This is to ensure that the script's desired umask is not
    visible to the user.

    :param override: non-script-default umask value to use
    :type override: int
    """
    try:
        if override is not None:
            old_umask = os.umask(override)
        else:
            old_umask = os.umask(DEFAULT_UMASK)
        yield
    finally:
        os.umask(old_umask)
