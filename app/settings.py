from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """App settings"""

    database_dsn: PostgresDsn
    google_sheet_key: str = None
    telegram_bot_token: str = None


settings = Settings()
