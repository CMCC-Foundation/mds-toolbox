import logging

from mds.conf import settings
from mds.core import mds_s3
from mds.core import wrapper
from mds.utils.log import configure_logging

logger = logging.getLogger(settings.LOGGER_NAME)


def setup(**kwargs) -> None:
    """
    General mds-toolbox setup

    Args:
        **kwargs: extra arguments to apply as app settings
    """
    settings.configure(**kwargs)
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING, settings.LOG_LEVEL)
