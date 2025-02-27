import logging.config
import datetime
import os

DEFAULT_LEVEL = logging.INFO


def get_my_fmt():
    return logging.Formatter(
        fmt="[%(asctime)s] - %(levelname)s: %(message)s",
        # TODO try to enable it only if logging level is DEBUG
        # fmt="[%(asctime)s] - %(levelname)s - %(name)s.%(funcName)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )


def set_level(level: int) -> None:
    """
    :param level: Logging level from 1 (CRITICAL) to 5 (DEBUG). Default is set to 4 (INFO)
    """
    root_logger = logging.getLogger()

    logger_level = (6 - level) * 10
    root_logger.setLevel(logger_level)


def add_file_handler(
    my_logger: logging.Logger = None, log_filename: str = None, log_dir: str = None
) -> None:
    """
    Add a file handler to the python logging module
    :param my_logger: logger to update with file handler
    :param log_filename: Name of log file
    :param log_dir: Path of the dir where store the file
    """
    if log_dir is None:
        log_dir = f"{os.getcwd()}/.log"
    os.makedirs(log_dir, exist_ok=True)

    if log_filename is None:
        log_filename = f"log_{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}.txt"

    log_file = os.path.join(log_dir, log_filename)

    my_fmt = get_my_fmt()

    # create file handler with my formatter
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(my_fmt)

    # enable file handler
    if not my_logger:
        print("Configuring root logger")
        my_logger = logging.getLogger()
    my_logger.addHandler(file_handler)


def set_up(name=None) -> logging.Logger:
    """
    Prepares a basic configuration of python logging module with StreamHandler to stderr using a personal formatter.
    Can be imported into the main script of the project
    """
    my_logger = logging.getLogger(name)
    # my_logger.propagate = False
    my_fmt = get_my_fmt()

    # Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
    my_logger.setLevel(DEFAULT_LEVEL)

    # Create stream handler with my formatter (as default print to stderr)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(my_fmt)

    # Enable stream handler
    my_logger.addHandler(stream_handler)
    return my_logger
