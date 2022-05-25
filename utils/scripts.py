import time
from datetime import timedelta
from functools import wraps
from typing import Callable

from sqlmodel import SQLModel

from app.database import engine
from app.logger import logger


def script(interval: timedelta):
    """
    Decorator for entrypoint scripts. Create models in database if they not exist,
    start safe busy-loop with given interval, logs raised errors
    """

    SQLModel.metadata.create_all(engine)

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    function(*args, **kwargs)
                except Exception as e:
                    logger.error(e, exc_info=True)

                time.sleep(interval.total_seconds())

        return wrapper

    return decorator
