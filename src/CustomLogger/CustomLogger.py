import logging
from .CustomFormatter import CustomFormatter

def CustomLogger(name: 'str') -> 'logging.Logger':
    """ Creates a custom formatted logger named <name> """

    # Create logger with "someName"
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger
