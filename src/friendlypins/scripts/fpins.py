"""Command line interface for the friendly pins APIs"""
#pragma: no cover
import argparse
import logging
import shlex
import sys
from friendlypins.utils.console_actions import download_thumbnails

def _download_thumbnails(args):
    """Callback for performing the thumbnail download operation

    :param args: Command line arguements customizing the behavior of the action
    :returns: zero on success, non-zero on failure
    :rtype: :class:`int`
    """
    return download_thumbnails(args.token, args.board, args.path)


def get_args(args):
    """Helper method used to parse command line parameters

    :param str args:
        optional command line arguements to be parsed
        if not provided, args will be parsed from the console
    :returns: parsed arguments
    :rtype: :class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Tool for interacting with Pinterest"
    )

    # Global options
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0)
    parser.add_argument(
        '--token', '-t',
        required=True,
        help="Pinterest API token to use for authentication")
    sub_commands = parser.add_subparsers()

    # Thumnail Downloader subparser
    desc = 'Downloads thumbnail images from pins'
    thumbnails_cmd = sub_commands.add_parser(
        'download_thumbnails',
        aliases=['dt'],
        description=desc,
        help=desc)
    thumbnails_cmd.set_defaults(func=_download_thumbnails)

    thumbnails_cmd.add_argument(
        '--board', '-b',
        required=True,
        help="Name of the board where the pins to download are located",
    )
    thumbnails_cmd.add_argument(
        '--path', '-p',
        required=True,
        help="Path to the folder where thumbnails are to be downloaded",
    )

    # If we've been given debugging arguments, convert them to the
    # format argparse expects
    if args:
        args = shlex.split(args)

    # By default, if no arguments are given, show online help
    if len(sys.argv) <= 1 and not args:
        args = ["-h"]

    # parse command line args
    return parser.parse_args(args)


def configure_logging(verbosity):
    """Configures the global logger for the application

    :param int verbosity:
        numeric value for the verbosity level for the log
        the larger the number, the more verbose the output
    """
    # Configure a console logger for everything that should show up
    # on the shell to the user
    console_handler = logging.StreamHandler(sys.stdout)

    # Configure a file logger for all verbose output to be streamed
    # to regardless of the source
    file_handler = logging.FileHandler('friendlypins.log', 'w')
    fmt = '%(asctime)s %(levelname)s (%(name)s.%(funcName)s) %(message)s'
    file_formatter = logging.Formatter(fmt=fmt)
    file_handler.setFormatter(file_formatter)


    # Make sure we capture everything with the global logger
    global_log = logging.getLogger()
    global_log.setLevel(logging.DEBUG)

    global_log.addHandler(file_handler)

    # Next, create our application logger here, and configure
    # it's verbosity based on user input
    log = logging.getLogger('friendlypins')
    if verbosity == 0:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.DEBUG)

    # Make sure we hook our console loggers to the appropriate logger
    # based on the level of verbosity the user has requested
    if verbosity < 2:
        log.addHandler(console_handler)
    else:
        global_log.addHandler(console_handler)


def main(args=None):
    """Entry point function

    :params str args:
        sample command line parameters to use when launching the tool
        used for debug and testing purposes only
        When not provided, arguments will be parsed from the command line

    :returns: error code produced by completing the given operation

    :rtype: :class:`int`
    """
    log = logging.getLogger(__name__)
    try:
        parser = get_args(args)
        configure_logging(parser.verbose)
        retval = parser.func(parser)
        if retval == 0:
            log.info("Operation completed successfully!")
        return retval
    except:  # pylint: disable=bare-except
        log.error("Critical error processing command")
        log.error("See verbose output for details")
        log.debug("Details: ", exc_info=True)
        return -1

if __name__ == "__main__":
    pass
