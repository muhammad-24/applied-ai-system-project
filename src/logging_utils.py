"""Simple file + console logging for the recommender system.

Every recommendation run is recorded to logs/recommender.log so there is
an audit trail of what was asked, what came back, and any warnings.
"""

import logging
import os

LOG_DIR = "logs"
LOG_PATH = os.path.join(LOG_DIR, "recommender.log")


def get_logger(name: str = "recommender") -> logging.Logger:
    """Return a configured logger that writes to file and console."""
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:  # avoid duplicate handlers on repeated calls
        return logger
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    return logger