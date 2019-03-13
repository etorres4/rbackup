import subprocess


# ========== Constants ==========
_RSYNC_BIN = '/usr/bin/rsync'


# ========== Functions ==========
def rsync(*args):
    """Run an rsync command.

    :param args: all arguments to pass to rsync
    :type args: str
    :raises: subprocess.CalledProcessError if rsync process failed
    """
    cmd = [_RSYNC_BIN, *args]
    subprocess.run(cmd, capture_output=True, check=True)
