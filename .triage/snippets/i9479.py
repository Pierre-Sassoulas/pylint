"""Repro attempt for the 'static test for a docker' report.

The reporter's file imported two local modules; ``Base`` is inlined
here and ``get_attributes`` stubbed, which is the only change.
"""

import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ARRAY, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def get_attributes(obj):
    return str(obj)


class DistributionDataset(Base):
    """Definition of the distribution table"""

    __tablename__ = "distribution_table"

    unique_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime)
    assets: Mapped[List[str]] = mapped_column(ARRAY(String))
    distribution: Mapped[List[float]] = mapped_column(ARRAY(Float))

    def __repr__(self) -> str:
        return get_attributes(self)
