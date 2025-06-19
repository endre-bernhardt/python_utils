import logging
import os
import sys

def get_logger(name=None, level=logging.INFO, log_to_file=False, log_dir="/var/log/va"):
    """
    Sets up a flexible logger for use in Flask apps, CLI scripts, or any multi-module Python project.

    This logger:
    - Clears existing handlers to avoid duplicate logs (especially helpful in containerized environments)
    - Outputs to stdout by default
    - Optionally writes logs to a rotating file in a given directory

    Args:
        name (str): Logger name. If None, root logger is used.
        level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
        log_to_file (bool): Whether to also log to a file.
        log_dir (str): Directory for log files if log_to_file is enabled.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Remove any existing handlers to prevent duplicates (common in Flask or reloaded apps)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(level)

    # Common formatter for all outputs
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler (stdout)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Optional file logging
    if log_to_file:
        try:
            os.makedirs(log_dir, exist_ok=True)
            log_file_path = os.path.join(log_dir, f"{name or 'root'}.log")
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")

    # Prevent logs from bubbling up to the root logger
    logger.propagate = False

    return logger

