import logging
import traceback

from mds.mng.cli import cli

logger = logging.getLogger("mds")


def start_from_command_line_interface():
    try:
        cli()
    except Exception as e:
        logger.debug(traceback.format_exc())
        logger.error(e)
        exit(1)
