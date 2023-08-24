import datetime as dt
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .courier import Courier
    from .region import Region


class Shift(Base):
    __tablename__ = 'shifts'

    shift_id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    region_id: Mapped[UUID] = mapped_column(ForeignKey('regions.region_id'))
    date: Mapped[dt.date]
    start_time: Mapped[dt.time]
    end_time: Mapped[dt.time]

    couriers: Mapped[list['Courier']] = relationship(
        secondary='couriers_shifts',
        back_populates='shifts',
        lazy='selectin'
    )
    region: Mapped['Region'] = relationship(back_populates='shifts')
