import logging
import sys

logger = logging.getLogger("ks-technical-task")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "{asctime}.{msecs:03.0f} [{levelname}] {message}",
    datefmt="%d.%m.%Y %H:%M:%S",
    style="{",
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
