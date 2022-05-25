from datetime import datetime
from decimal import Decimal
from functools import lru_cache
from xml.etree import ElementTree

import requests

USD_ID = "R01235"


# use lru_cache to avoid spamming
@lru_cache(maxsize=1)
def get_usdrub_rate(date: datetime.date) -> Decimal:
    """Get cbrf's USDRUB rate for given date"""

    params = {"date_req": date.strftime("%d/%m/%Y")}
    response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp", params)
    response.raise_for_status()

    tree = ElementTree.fromstring(response.content)
    rate_str = tree.find(f".//Valute[@ID='{USD_ID}']/Value").text

    return Decimal(rate_str.replace(",", "."))
