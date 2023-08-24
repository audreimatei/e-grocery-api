from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config import CourierType

from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .shift import Shift


class Courier(Base):
    __tablename__ = 'couriers'

    courier_id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    courier_type: Mapped[CourierType]

    orders: Mapped[list['Order']] = relationship(
        back_populates='courier',
        lazy='selectin'
    )
    shifts: Mapped[list['Shift']] = relationship(
        secondary='couriers_shifts',
        back_populates='couriers',
        lazy='selectin'
    )

    @property
    def weight(self) -> int:
        return sum(order.weight for order in self.orders)


couriers_shifts = Table(
    'couriers_shifts',
    Base.metadata,
    Column('courier_id', ForeignKey('couriers.courier_id'), primary_key=True),
    Column('shift_id', ForeignKey('shifts.shift_id'), primary_key=True)
)
