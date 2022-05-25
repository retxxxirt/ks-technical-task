from datetime import datetime

from app.logger import logger
from app.refresher import cbrf
from app.refresher.backends import BaseBackend
from app.refresher.extractors import BaseExtractor
from app.schemas import BaseOrder


class Refresher:
    """Refresh orders from given extractor for given backend"""

    def __init__(self, extractor: BaseExtractor, backend: BaseBackend):
        self._extractor = extractor
        self._backend = backend

    @staticmethod
    def _update_orders(orders: list[BaseOrder]) -> list[BaseOrder]:
        """Update orders with price_rub field, based on cbrf's rate and price_usd field"""

        updated_orders = []
        now_date = datetime.now().date()
        usdrub_rate = cbrf.get_usdrub_rate(now_date)

        for order in orders:
            order.price_rub = order.price_usd * usdrub_rate

            # we need recreate order to enforce price_rub field validation
            updated_order = BaseOrder(**order.dict())
            updated_orders.append(updated_order)

        return updated_orders

    def refresh_orders(self):
        """Extract, update and refresh orders"""

        orders = self._extractor.extract_orders()
        orders = self._update_orders(orders)

        self._backend.refresh_orders(orders)

        logger.info(f"Successfully refreshed {len(orders)} order(s)")
