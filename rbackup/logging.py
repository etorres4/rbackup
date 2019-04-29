"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.logging
    :synopsis: library for common logging constants
"""

import logging
import sys

# ========== Constants ==========
# ----- Console Formatters -----
_CONSOLE_FORMAT = "==> %(levelname)s %(message)s"
CONSOLE_FORMATTER = logging.Formatter(_CONSOLE_FORMAT)


# ========== Functions ==========
def retrieve_console_handlers(*, debug=False):
    """Retrieve a pair of logging handlers configured for console output.

    :param debug: should logging.DEBUG level messages be recorded? (default: ``False``)
    :type debug: bool
    :return: tuple of ``logging.StreamHandler``s for stdout and stderr
    """
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(_CONSOLE_FORMAT)
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)

    if debug:
        stdout_handler.setLevel(logging.DEBUG)
    else:
        stdout_handler.setLevel(logging.INFO)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(_CONSOLE_FORMAT)

    return stdout_handler, stderr_handler
