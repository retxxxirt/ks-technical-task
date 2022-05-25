from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.database import DatabaseRecipient, DatabaseOrder, DatabaseNotifiedState
from app.schemas import Provider, BaseRecipient, NotificationData


class BaseBackend(ABC):
    """Abstract backend"""

    @abstractmethod
    def save_recipient(self, provider: Provider, provider_id: str):
        """Must create recipient with given data at the backend"""

    @abstractmethod
    def _get_provider_recipients(self, platform: Provider) -> Iterable[BaseRecipient]:
        """Must yield all recipients for given provider"""

    @abstractmethod
    def _get_recipient_notification(self, recipient: BaseRecipient) -> NotificationData | None:
        """Must return NotificationData object with actual orders data or None for recipient"""

    @abstractmethod
    def mark_notification_sent(self, notification: NotificationData):
        """Must mark notification at the backend as sent"""

    def get_notifications_for_provider(self, provider: Provider) -> Iterable[NotificationData]:
        """Yield all actual notifications for given provider"""

        for recipient in self._get_provider_recipients(provider):
            notification = self._get_recipient_notification(recipient)

            if notification is not None:
                yield notification


class DatabaseBackend(BaseBackend):
    """Database backend implementation"""

    def __init__(self, engine: Engine):
        self._engine = engine
        self._session = None

    def save_recipient(self, provider: Provider, provider_id: str):
        """Create recipient if it doesn't exist"""

        with Session(self._engine) as self._session:
            recipient = DatabaseRecipient(provider=provider, provider_id=provider_id)

            try:
                self._session.add(recipient)
                self._session.commit()
            except IntegrityError:
                # skip if recipient already exists
                pass

    def _get_provider_recipients(self, provider: Provider) -> Iterable[DatabaseRecipient]:
        """Yield all recipients for given provider"""

        condition = DatabaseRecipient.provider == provider
        yield from self._session.query(DatabaseRecipient).where(condition)

    def _get_recipient_notification(self, recipient: DatabaseRecipient) -> NotificationData | None:
        """
        Generate NotificationData with actual orders
        for recipient, None if there are no actual orders
        """

        # select orders and full join notified states
        query = self._session.query(DatabaseOrder)
        order_condition = DatabaseOrder.order_id == DatabaseNotifiedState.order_id
        query = query.outerjoin(DatabaseNotifiedState, order_condition)

        # filter only records without notified state
        query = query.where(DatabaseNotifiedState.order_id.is_(None))

        # join target recipient
        provider_condition = DatabaseRecipient.provider == recipient.provider
        provider_id_condition = DatabaseRecipient.provider_id == recipient.provider_id
        query = query.join(DatabaseRecipient, provider_condition & provider_id_condition)

        # put all unsent orders in two queries - today's supplies and overdue supplies
        today_orders_query = query.where(DatabaseOrder.supply_date == datetime.now().date())
        overdue_orders_query = query.where(DatabaseOrder.supply_date < datetime.now().date())

        today_orders = list(today_orders_query)
        overdue_orders = list(overdue_orders_query)

        if len(today_orders) or len(overdue_orders):
            return NotificationData(recipient, today_orders, overdue_orders)

    def mark_notification_sent(self, notification: NotificationData):
        """Create DatabaseNotifiedState entries for recipient and all orders in notification"""

        with Session(self._engine) as self._session:
            notified_states = []

            for order in notification.today_orders + notification.overdue_orders:
                notified_state = DatabaseNotifiedState(
                    order_id=order.order_id,
                    recipient_provider=notification.recipient.provider,
                    recipient_provider_id=notification.recipient.provider_id,
                )
                notified_states.append(notified_state)

            self._session.add_all(notified_states)
            self._session.commit()

    def get_notifications_for_provider(self, provider: Provider) -> Iterable[NotificationData]:
        """
        Yield all actual notifications for given provider.
        This method wraps parent's method with session context
        """

        with Session(self._engine) as self._session:
            yield from super().get_notifications_for_provider(provider)
