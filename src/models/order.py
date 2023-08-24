import datetime as dt
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import geoalchemy2
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src import schemas

from . import types
from .base import Base

if TYPE_CHECKING:
    from .courier import Courier
    from .item import Item
    from .region import Region


class Order(Base):
    __tablename__ = 'orders'

    order_id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    courier_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('couriers.courier_id')
    )
    delivery_region_id: Mapped[UUID] = mapped_column(
        ForeignKey('regions.region_id')
    )
    delivery_address: Mapped[str]
    _delivery_location: Mapped[types.Point] = mapped_column(types.Point)  # type: ignore
    created_at: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.utcnow()
    )
    completed_at: Mapped[dt.datetime | None] = mapped_column(default=None)

    courier: Mapped['Courier'] = relationship(back_populates='orders')
    delivery_region: Mapped['Region'] = relationship(back_populates='orders')
    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='order',
        lazy='subquery'
    )

    @property
    def delivery_location(self) -> schemas.GeoPoint:
        longitude, latitude = (
            geoalchemy2.shape.to_shape(self._delivery_location).coords[0]
        )
        return schemas.GeoPoint(latitude=latitude, longitude=longitude)

    @delivery_location.setter
    def delivery_location(self, geo_point: schemas.GeoPoint) -> None:
        self._delivery_location = geoalchemy2.WKTElement(
            f'POINT({geo_point.longitude} {geo_point.latitude})'
        )

    @property
    def cost(self) -> int:
        return sum(
            order_item.item.price * order_item.amount
            for order_item in self.order_items
        )

    @property
    def weight(self) -> int:
        return sum(
            order_item.item.weight * order_item.amount
            for order_item in self.order_items
        )


class OrderItem(Base):
    __tablename__ = 'orders_items'

    order_id: Mapped[UUID] = mapped_column(
        ForeignKey('orders.order_id'),
        primary_key=True
    )
    item_id: Mapped[UUID] = mapped_column(
        ForeignKey('items.item_id'),
        primary_key=True
    )
    amount: Mapped[int]

    item: Mapped['Item'] = relationship(
        back_populates='order_associations',
        lazy='subquery'
    )
    order: Mapped['Order'] = relationship(
        back_populates='order_items',
        lazy='subquery'
    )
