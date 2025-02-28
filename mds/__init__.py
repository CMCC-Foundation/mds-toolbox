from mds.conf import settings

from mds.core import mds_s3
from mds.core import wrapper


def setup(**kwargs) -> None:
    """
    General mds-toolbox setup

    Args:
        **kwargs: extra arguments to apply as app settings
    """
    settings.configure(**kwargs)
