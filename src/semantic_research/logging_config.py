import logging
import sys
from typing import Optional

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

def configure_logging(level: str = "INFO", *, logger_name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Avoid duplicate handlers in notebooks/tests
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False
    return logger
