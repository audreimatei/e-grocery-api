from pydantic import UUID4

from .base import GeoPoint, ORJSONModel


class RegionBase(ORJSONModel):
    name: str
    geo_polygon: list[GeoPoint]


class Region(RegionBase):
    region_id: UUID4

    class Config:
        orm_mode = True


class RegionCreate(RegionBase):
    pass


class Regions(ORJSONModel):
    regions: list[Region]


class RegionsLimitOffset(Regions):
    limit: int
    offset: int

    class Config:
        orm_mode = True
