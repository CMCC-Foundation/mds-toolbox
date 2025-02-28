from mds.conf import settings


def setup(**kwargs) -> None:
    """
    General mds-toolbox setup

    Args:
        **kwargs: extra arguments to apply as app settings
    """
    settings.configure(**kwargs)
