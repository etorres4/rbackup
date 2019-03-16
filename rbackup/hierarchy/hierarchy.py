"""
.. author:: Eric Torres
.. module:: rbackup.hierarchy.hierarchy
    :synopsis: Classes for creating the backup hierarchy.
"""


# ========== Classes ==========
class Hierarchy:
    """A class for organizing the backup root hierarchy."""

    def __init__(self, dest):
        """Default constructor for the Hierarchy class.

        Example
        -------
        >>> hier = Hierarchy('/tmp')
        >>> hier.path
        '/tmp'

        :param dest: the root directory of the backup hierarchy
        :type dest: str, bytes
        """
        self.dest = dest

    @property
    def path(self):
        """Return the base directory of this hierarchy.

        Example
        -------
        >>> hier = Hierarchy('/tmp')
        >>> hier.path
        '/tmp'

        :rtype: str
        """
        return self.dest


# ========== Functions ==========
if __name__ == "__main__":
    import doctest

    doctest.testmod()
