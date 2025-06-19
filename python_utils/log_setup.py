import logging
import sys

def get_logger(name=None, level=logging.INFO):
    """
    Sets up a logger that works in Flask, plain Python, and multi-module apps.
    Clears existing handlers and attaches a StreamHandler to stdout.

    Args:
        name (str): Logger name, defaults to root if None.
        level (int): Logging level, default is INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Clear existing handlers (especially useful in containers / Flask)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Setup handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(level)
    logger.propagate = False  # Don't bubble up to root again (avoids duplication in Flask)

    return logger

