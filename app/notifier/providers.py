from abc import ABC, abstractmethod

import telebot
from telebot.types import Message

from app.notifier.backends import BaseBackend
from app.notifier.serializers import TelegramNotificationSerializer
from app.schemas import Provider, NotificationData


class BaseProvider(ABC):
    """Abstract notifications' provider class"""

    name: Provider = None

    @abstractmethod
    def send_notification(self, notification: NotificationData):
        """Must send notification to recipient through that provider"""


class TelegramProvider(BaseProvider):
    """Telegram provider implementation"""

    name: Provider = Provider.telegram

    def __init__(self, bot_token: str):
        """Connect to telegram bots api with bot_token through telebot"""
        self._bot = telebot.TeleBot(bot_token)

    def send_notification(self, notification: NotificationData):
        """Send serialized notification to recipient"""

        message = TelegramNotificationSerializer(notification).serialize()
        self._bot.send_message(notification.recipient.provider_id, message, parse_mode="HTML")


class BasePollingClient(ABC):
    """Abstract polling client"""

    provider: Provider = None

    def __init__(self, backend: BaseBackend):
        self._backend = backend

    def save_recipient(self, recipient_id: str):
        """Save contacted recipient to backend"""
        self._backend.save_recipient(self.provider, recipient_id)

    @abstractmethod
    def start_polling(self):
        """Must start provider's polling"""


class TelegramPollingClient(BasePollingClient):
    """Telegram polling client implementation"""

    provider: Provider = Provider.telegram

    def __init__(self, backend: BaseBackend, bot_token: str):
        """Connect to telegram bots api with bot_token and register _save_recipient as handler"""

        super().__init__(backend)

        self._bot = telebot.TeleBot(bot_token)
        self._bot.register_message_handler(self._save_recipient)

    def _save_recipient(self, message: Message):
        """Save any contacted recipient to backend"""
        self.save_recipient(str(message.chat.id))

    def start_polling(self):
        """Star telebot polling"""
        self._bot.polling()
