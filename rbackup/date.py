import datetime
import os.path

def gen_datetime(*paths):
    """Generate a path for a backup directory that contains
    the current date and time.

    :param paths: paths to prepend to the result
    :type paths: str, bytes, or path-like object
    :returns: stuff
    """
    return os.path.join(*paths, datetime.datetime.utcnow().isoformat())
