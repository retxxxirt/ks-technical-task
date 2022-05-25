from datetime import timedelta

from app.database import engine
from app.refresher.backends import DatabaseBackend
from app.refresher.extractors import GSExtractor
from app.refresher.refresher import Refresher
from app.settings import settings
from utils.scripts import script


@script(interval=timedelta(seconds=5))
def refresh_orders():
    """Refresh orders with GSExtractor and DatabaseBackend"""

    extractor = GSExtractor(settings.google_sheet_key)
    backend = DatabaseBackend(engine)

    refresher = Refresher(extractor, backend)
    refresher.refresh_orders()


if __name__ == "__main__":
    refresh_orders()
