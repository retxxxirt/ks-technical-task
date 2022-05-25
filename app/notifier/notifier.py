from app.logger import logger
from app.notifier.backends import BaseBackend
from app.notifier.providers import BaseProvider


class Notifier:
    """Notify all given providers with data from given backend"""

    def __init__(self, providers: list[BaseProvider], backend: BaseBackend):
        self._providers = providers
        self._backend = backend

    def send_notifications(self):
        """Send notifications for every recipient for every provider and mark them as sent"""

        for provider in self._providers:
            notifications = self._backend.get_notifications_for_provider(provider.name)
            notifications_counter = 0

            for notification in notifications:
                provider.send_notification(notification)
                self._backend.mark_notification_sent(notification)

                notifications_counter += 1

            logger.info(f"Sent {notifications_counter} actual notification(s) via {provider.name}")
