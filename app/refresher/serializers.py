from abc import ABC, abstractmethod
from typing import Any

from app.schemas import BaseOrder


class BaseOrderSerializer(ABC):
    """Base order serializer class"""

    def __init__(self, raw_order: Any):
        self._raw_order = raw_order

    @abstractmethod
    def serialize(self) -> BaseOrder:
        """Must return serialized BaseOrder from raw_data"""


class GSOrderSerializer(BaseOrderSerializer):
    """Google sheets order serializer implementation"""

    def __init__(self, raw_order: list[str]):
        """Override for typing purposes"""
        super().__init__(raw_order)

    def serialize(self) -> BaseOrder:
        """Serialize google sheet's order to BaseOrder"""
        fields = ("table_id", "order_id", "price_usd", "supply_date")
        return BaseOrder.parse_obj(dict(zip(fields, self._raw_order)))
