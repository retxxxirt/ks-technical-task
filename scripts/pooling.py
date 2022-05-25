from datetime import timedelta

from app.database import engine
from app.notifier.backends import DatabaseBackend
from app.notifier.providers import TelegramPoolingClient
from app.settings import settings
from utils.scripts import script


@script(interval=timedelta(seconds=5))
def start_pooling():
    """Start telegram bot pooling and save all contacted users as recipients"""

    backend = DatabaseBackend(engine)
    pooling_client = TelegramPoolingClient(backend, settings.telegram_bot_token)

    pooling_client.start_pooling()


if __name__ == "__main__":
    start_pooling()
