"""Entry point to mds-toolbox API"""

import functools

import mds


def init_app():
    """Initialize the application functions before the execution"""

    def decorated(func):
        @functools.wraps(func)
        def setup(**kwargs):
            """
            Extract app settings and configure application setup, then start mds functions.

            Args:
                **kwargs: Arbitrary keyword arguments passed to the function.
            """
            user_settings = dict()
            # Assume that upper settings are app settings related
            upper_keys = [k for k in kwargs.keys() if k.isupper()]

            # Remove upper settings from plot arguments to avoid crash in PlotSettings class
            for k in upper_keys:
                user_settings[k] = kwargs.pop(k)

            # Perform general app initialization
            mds.setup(**user_settings)

            # Start application
            return func(**kwargs)

        # Return the setup function which wraps the original function
        return setup

    # Return the decorator function
    return decorated
