from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .order import Order, OrderItem

class Item(Base):
    __tablename__ = 'items'

    item_id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    weight: Mapped[int]
    price: Mapped[int]

    order_associations: Mapped[list['OrderItem']] = relationship(
        back_populates='item',
        lazy='subquery'
    )