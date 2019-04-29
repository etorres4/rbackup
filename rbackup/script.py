"""
.. moduleauthor:: Eric Torres
.. module:: rbackup.script
    :synopsis: library for common script operations
"""

import logging
from subprocess import CalledProcessError

import rbackup.config.config_files as config
import rbackup.rsync
import rbackup.system as system

# ========== Constants ==========
# ----- Error Codes -----
E_INVALID_SNAPSHOT_NAME = 2
E_PERMISSION = 13


# ========== Logging Setup ===========
syslog = logging.getLogger(__name__)


# ========== Functions ==========
def do_backup(repository, parsed_config, args, extra_rsync_opts=None):
    """Run a backup operation.

    A backup operation requires a repository, config options to read from, and the
    arguments that were passed when the script was started.

    It is up to the caller to decide on how to instantiate the ``Repository`` object.

    :param repository: repository to operate on
    :type repository: ``rbackup.struct.repository.Repository`` object
    :param parsed_config: config file parser
    :type parsed_config: ``configparser.ConfigParser`` object
    :param args: arguments passed when the script was called
    :type args: ``argparse.Namespace`` object
    :param extra_rsync_opts: options to pass to rsync that weren't included
        in args (default: ``None``)
    :type extra_rsync_opts: iterable
    """
    rsync_opts = config.load_list_from_option(
        parsed_config,
        section="main",
        option="RsyncOptions",
        fallback=rbackup.rsync.DEFAULT_RSYNC_OPTS.copy(),
    )

    if args.extra_rsync_opts is not None:
        rsync_opts.extend(args.extra_rsync_opts)

    if extra_rsync_opts is not None:
        rsync_opts.extend(rsync_opts)

    # We want to iterate through the repository and create the --link-dest
    # options before creating the new snapshot
    link_dests = tuple(f"--link-dest={s.path}" for s in repository)

    with system.change_umask(
        args.umask
    ), config.merge_include_files() as include_file, config.merge_exclude_files() as exclude_file:
        try:
            curr_snapshot = repository.create_snapshot(args.name)
            rbackup.rsync.rsync(
                *rsync_opts,
                f"--files-from={include_file}",
                f"--exclude-from={exclude_file}",
                *link_dests,
                "/",
                str(curr_snapshot),
            )
        except ValueError as e:
            syslog.critical(e)
            exit(E_INVALID_SNAPSHOT_NAME)
        except CalledProcessError as e:
            syslog.critical("Backup process failed")
            syslog.critical(f"Failing command: {e.cmd}")
            syslog.critical(e.stderr)
            exit(e.returncode)
