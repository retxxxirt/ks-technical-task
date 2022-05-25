from datetime import timedelta

from app.database import engine
from app.notifier.backends import DatabaseBackend
from app.notifier.notifier import Notifier
from app.notifier.providers import TelegramProvider
from app.settings import settings
from utils.scripts import script


@script(interval=timedelta(seconds=10))
def send_notifications():
    """Notify all telegram recipients using data from DatabaseBackend"""

    provider = TelegramProvider(settings.telegram_bot_token)
    backend = DatabaseBackend(engine)

    notifier = Notifier([provider], backend)
    notifier.send_notifications()


if __name__ == "__main__":
    send_notifications()
