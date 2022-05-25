import decimal
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel
from pydantic.validators import decimal_validator


class Date(date):
    """Pydantic's date field implementation with given format"""

    format = "%d.%m.%Y"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: str | date) -> date:
        if isinstance(value, str):
            return datetime.strptime(value, cls.format).date()
        return value


class Money(Decimal):
    """Pydantic's money field implementation with given precision"""

    quant = Decimal("0.01")

    @classmethod
    def __get_validators__(cls):
        yield decimal_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: Decimal) -> Decimal:
        return value.quantize(cls.quant, decimal.ROUND_HALF_UP)


class Provider(str, Enum):
    """Providers enum"""

    telegram = "telegram"


class BaseOrder(BaseModel):
    """Base order schema"""

    table_id: int
    order_id: int
    price_usd: Money
    price_rub: Money = None
    supply_date: Date


class BaseRecipient(BaseModel):
    """Base recipient schema"""

    provider: Provider
    provider_id: str


class BaseNotifiedState(BaseModel):
    """Base notified state schema for every order and recipient"""

    order_id: int
    recipient_provider: Provider
    recipient_provider_id: str


@dataclass
class NotificationData:
    """Notification data class"""

    recipient: BaseRecipient
    today_orders: list[BaseOrder]
    overdue_orders: list[BaseOrder]
