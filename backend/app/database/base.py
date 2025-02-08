from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime


class Base(DeclarativeBase):
    created_at = Column(
        DateTime(timezone=True), nullable=False,
        default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )
