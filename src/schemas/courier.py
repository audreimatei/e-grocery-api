from pydantic import UUID4

from src.config import CourierType

from .base import ORJSONModel


class CourierBase(ORJSONModel):
    courier_type: CourierType


class Courier(CourierBase):
    courier_id: UUID4

    class Config:
        orm_mode = True


class CourierCreate(CourierBase):
    pass


class Couriers(ORJSONModel):
    couriers: list[Courier]


class CouriersLimitOffset(Couriers):
    limit: int
    offset: int

    class Config:
        orm_mode = True


class CourierMetaInfo(ORJSONModel):
    earnings: int
    rating: float
