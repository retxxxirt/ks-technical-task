from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy.engine import Engine
from sqlmodel import Session

from app.database import DatabaseOrder, DatabaseNotifiedState
from app.schemas import BaseOrder


class BaseBackend(ABC):
    """Abstract backend"""

    @abstractmethod
    def _clear_unlisted_orders(self, listed_ids: list[int]):
        """Must clear all unlisted orders from backend"""

    @abstractmethod
    def _refresh_order(self, order: BaseOrder):
        """Must refresh single order"""

    def refresh_orders(self, orders: list[BaseOrder]):
        """Process all orders, then clear unlisted at this backend"""

        listed_ids = []

        for order in orders:
            self._refresh_order(order)
            listed_ids.append(order.order_id)

        self._clear_unlisted_orders(listed_ids)


class DatabaseBackend(BaseBackend):
    """Database backend implementation"""

    def __init__(self, engine: Engine):
        self._engine = engine
        self._session = None

    def _clear_unlisted_orders(self, listed_ids: list[int]):
        """Clear unlisted orders from database"""

        condition = DatabaseOrder.order_id.not_in(listed_ids)
        self._session.query(DatabaseOrder).where(condition).delete()

    def _clear_notified_states(self, order: DatabaseOrder):
        """Clear all notified states for order"""

        condition = DatabaseNotifiedState.order_id == order.order_id
        self._session.query(DatabaseNotifiedState).where(condition).delete()

    def _refresh_order(self, order: BaseOrder):
        """Update order if it exists in database or create it"""

        db_order = self._session.query(DatabaseOrder).get(order.order_id)

        if db_order is None:
            db_order = DatabaseOrder(**order.dict())
        else:
            # clear all notified states if supply_date changed
            # and order has not been supplied before today
            if order.supply_date != db_order.supply_date:
                if db_order.supply_date >= datetime.now().date():
                    self._clear_notified_states(db_order)

            for field, value in order.dict().items():
                setattr(db_order, field, value)

        self._session.add(db_order)

    def refresh_orders(self, orders: list[BaseOrder]):
        """
        Process all orders, then clear unlisted at this backend. This method wraps
        parent's method with session context and commit session at the end
        """

        with Session(self._engine) as self._session:
            super().refresh_orders(orders)
            self._session.commit()
