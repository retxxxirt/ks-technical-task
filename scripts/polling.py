from datetime import timedelta

from app.database import engine
from app.notifier.backends import DatabaseBackend
from app.notifier.providers import TelegramPollingClient
from app.settings import settings
from utils.scripts import script


@script(interval=timedelta(seconds=5))
def start_polling():
    """Start telegram bot polling and save all contacted users as recipients"""

    backend = DatabaseBackend(engine)
    polling_client = TelegramPollingClient(backend, settings.telegram_bot_token)

    polling_client.start_polling()


if __name__ == "__main__":
    start_polling()
