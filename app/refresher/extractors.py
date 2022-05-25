import os
from abc import ABC, abstractmethod

import gspread
from pydantic import ValidationError

from app.logger import logger
from app.refresher.serializers import GSOrderSerializer
from app.schemas import BaseOrder


class BaseExtractor(ABC):
    """Abstract extractor class"""

    @abstractmethod
    def extract_orders(self) -> list[BaseOrder]:
        """Must extract orders from target source"""


class GSExtractor(BaseExtractor):
    """Google sheets extractor implementation"""

    credentials_path = "../../data/service_account.json"

    def __init__(self, sheet_key: str, header_height: int = 1):
        """Open google sheet by sheet_key, requires data/service_account.json file"""

        credentials_path = os.path.join(os.path.dirname(__file__), self.credentials_path)
        account = gspread.service_account(credentials_path)

        self._sheet = account.open_by_key(sheet_key).sheet1
        self._header_height = header_height

    def extract_orders(self) -> list[BaseOrder]:
        """Extract serialized data from google sheet"""

        orders = []
        raw_orders = self._sheet.get_values()[self._header_height :]

        for raw_order in raw_orders:
            try:
                order = GSOrderSerializer(raw_order).serialize()
            except ValidationError:
                logger.warning(f"Invalid row data: {raw_order}")
            else:
                orders.append(order)

        return orders
