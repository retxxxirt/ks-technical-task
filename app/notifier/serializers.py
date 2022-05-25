from abc import ABC, abstractmethod

from app.schemas import NotificationData, BaseOrder


class BaseNotificationSerializer(ABC):
    """Abstract notification serializer"""

    def __init__(self, notification: NotificationData):
        self._notification = notification

    @abstractmethod
    def serialize(self) -> str:
        """Must return serialized message"""


class TelegramNotificationSerializer(BaseNotificationSerializer):
    """Telegram notification serializer implementation"""

    def _order2string(self, order: BaseOrder, include_date: bool = False):
        """Convert order to string"""

        order_str = f"<code>{order.order_id}</code>"

        if include_date:
            date_str = order.supply_date.strftime("%d.%m.%Y")
            order_str = f"{order_str} ({date_str})"

        return order_str

    def serialize(self) -> str:
        """Serialize NotificationData in representative telegram message"""

        message_lines = []

        if len(self._notification.today_orders):
            message_lines.append("Сегодня ожидают поставки следующие заказы:")

            orders_strings = [self._order2string(o) for o in self._notification.today_orders]
            message_lines.append(", ".join(orders_strings))

        if len(self._notification.overdue_orders):
            message_lines.append("У следующих заказов истек срок поставки:")

            orders = self._notification.overdue_orders.copy()
            orders.sort(key=lambda o: o.supply_date)

            orders_strings = [self._order2string(o, include_date=True) for o in orders]
            message_lines.append(", ".join(orders_strings))

        return "\n".join(message_lines)
