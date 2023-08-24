import datetime as dt
from typing import Annotated

from pydantic import UUID4, Field

from .base import GeoPoint, ORJSONModel


class OrderItem(ORJSONModel):
    item_id: UUID4
    amount: Annotated[int, Field(ge=1)]

    class Config:
        orm_mode = True


class OrderBase(ORJSONModel):
    delivery_address: str
    delivery_location: GeoPoint
    order_items: list[OrderItem]


class Order(OrderBase):
    order_id: UUID4
    courier_id: UUID4 | None
    delivery_region_id: UUID4
    created_at: dt.datetime
    completed_at: dt.datetime | None
    cost: int
    weight: int

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    delivery_region_id: UUID4 | None


class Orders(ORJSONModel):
    orders: list[Order]


class OrdersLimitOffset(Orders):
    limit: int
    offset: int

    class Config:
        orm_mode = True
