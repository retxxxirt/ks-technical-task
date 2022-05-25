from sqlalchemy import PrimaryKeyConstraint
from sqlmodel import SQLModel, Field
from sqlmodel import create_engine

from app.schemas import BaseOrder, BaseRecipient, BaseNotifiedState
from app.settings import settings

engine = create_engine(settings.database_dsn)


class DatabaseOrder(BaseOrder, SQLModel, table=True):
    """Database order model"""

    __tablename__ = "orders"

    order_id: int = Field(primary_key=True)


class DatabaseRecipient(BaseRecipient, SQLModel, table=True):
    """Database recipient model"""

    __tablename__ = "recipients"
    __table_args__ = (PrimaryKeyConstraint("provider", "provider_id"),)


class DatabaseNotifiedState(BaseNotifiedState, SQLModel, table=True):
    """Database notified state for every order and recipient"""

    __tablename__ = "notified"

    __table_args__ = (
        PrimaryKeyConstraint(
            "order_id",
            "recipient_provider",
            "recipient_provider_id",
        ),
    )
