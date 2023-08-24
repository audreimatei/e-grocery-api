from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import geoalchemy2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src import schemas

from . import types
from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .shift import Shift


class Region(Base):
    __tablename__ = 'regions'

    region_id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str]
    _geo_polygon: Mapped[types.Polygon] = mapped_column(types.Polygon)  # type: ignore

    orders: Mapped[list['Order']] = relationship(
        back_populates='delivery_region',
        lazy='selectin'
    )
    shifts: Mapped[list['Shift']] = relationship(
        back_populates='region',
        lazy='selectin'
    )

    @property
    def geo_polygon(self) -> list[schemas.GeoPoint]:
        points: list[tuple[float, float]] = (
            geoalchemy2.shape.to_shape(self._geo_polygon).exterior.coords
        )
        return [
            schemas.GeoPoint(latitude=point[1], longitude=point[0])
            for point in points
        ]

    @geo_polygon.setter
    def geo_polygon(self, geo_polygon: list[schemas.GeoPoint]) -> None:
        points = ','.join(
            f'{geo_point.longitude} {geo_point.latitude}'
            for geo_point in geo_polygon
        )
        self._geo_polygon = geoalchemy2.WKTElement(f'POLYGON(({points}))')
