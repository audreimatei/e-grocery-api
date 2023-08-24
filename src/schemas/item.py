from typing import Annotated

from pydantic import UUID4, Field

from .base import ORJSONModel


class ItemBase(ORJSONModel):
    name: str
    weight: Annotated[int, Field(ge=1)]
    price: Annotated[int, Field(ge=1)]


class Item(ItemBase):
    item_id: UUID4

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    pass


class Items(ORJSONModel):
    items: list[Item]


class ItemsLimitOffset(Items):
    limit: int
    offset: int

    class Config:
        orm_mode = True
