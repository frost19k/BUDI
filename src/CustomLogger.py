### Adapted from https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output/56944256#56944256 ###

import emoji
import logging

class CustomFormatter(logging.Formatter):
    """ Logging Formatter to add colors and count warning / errors """

    colors = {
        "grey":"\x1b[0;37m",
        "green":"\x1b[0;32m",
        "blue":"\x1b[0;34m",
        "cyan":"\x1b[0;36m",
        "purple":"\x1b[0;35m",
        "yellow":"\x1b[0;33m",
        "red":"\x1b[0;31m",
        "bold_red":"\x1b[1;31m",
        "reset":"\x1b[0m"
    }

    log_HeadFormat = '%(asctime)s ⋞ {levelEmoji} ⋟ '

    FORMATS = {
        logging.DEBUG: log_HeadFormat.format(levelEmoji=emoji.emojize(':dashing_away:')) + '%(message)s' + colors['reset'],
        logging.INFO: log_HeadFormat.format(levelEmoji=emoji.emojize(':speech_balloon:')) + '%(msgC)s%(message)s' + colors['reset'],
        logging.WARNING: log_HeadFormat.format(levelEmoji=emoji.emojize(':bomb:')) + colors['yellow'] + '%(message)s' + colors['reset'],
        logging.ERROR: log_HeadFormat.format(levelEmoji=emoji.emojize(':anger_symbol:')) + colors['red'] + '%(message)s (%(filename)s:%(lineno)d)' + colors['reset'],
        logging.CRITICAL: log_HeadFormat.format(levelEmoji=emoji.emojize(':collision:')) + colors['bold_red'] + '%(message)s (%(filename)s:%(lineno)d)' + colors['reset'],
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        # formatter = logging.Formatter(log_fmt, datefmt='%I:%M:%S %p')
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def CustomLogger(name: 'str') -> 'logging.Logger':
    # Create logger with "someName"
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger

if __name__ == "__main__":
    c = CustomFormatter.colors

    logger = CustomLogger('myLogger')
    logger.debug(f'this is a debug message')
    logger.info(f'this is a grey info message', extra={'msgC':''})
    logger.info(f'this is a green info message', extra={'msgC':c['green']})
    logger.info(f'this is a cyan info message', extra={'msgC':c['cyan']})
    logger.warning(f'this is a warning message')
    logger.error(f'this is a error message')
    logger.critical(f'this is a critical message')
