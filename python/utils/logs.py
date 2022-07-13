"""

Project: Data Engineering Project
Author: Alessandro C.

Description:
Module with functions dedicated to produce and configure logs.

"""

import logging


def create_log(function: str, message: str, data: dict = None,
               log_level: str = 'INFO') -> None:
    """Build dictionary which ultimately will be used to build a log.

    :param function: Name of the function where the log is running
    :type function: str
    :param message: Informative value of what's going on at the specific moment
    the log is being used
    :type message: str
    :param data: Additional data to help understand the log message, defaults to
    None
    :type data: dict, optional
    """

    # Build base body for our logs
    log_content = {
        'function': function,
        'message': message
    }

    # Add additional data when received here in the function
    if data:
        log_content['data'] = data

    # Define the different functions we can use according to the level of the
    # log we need to use in the calling function
    logs = {
        'DEBUG': logging.debug,
        'INFO': logging.info,
        'WARNING': logging.warning,
        'ERROR': logging.error,
    }

    # Execute log
    logs[log_level](log_content)
