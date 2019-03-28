"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.snapshot
    :synopsis: Classes for creating the backup hierarchy.
"""
import logging

from rbackup.hierarchy.hierarchy import Hierarchy


# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Classes ==========
class Snapshot(Hierarchy):
    """Hierarchy for a single snapshot.
    Attributes
    ----------
    * path (inherited from Hierarchy)
    * name (inherited from Hierarchy)
    """

    def __init__(self, path):
        """Default constructor for the Snapshot class."""
        super().__init__(path)


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
