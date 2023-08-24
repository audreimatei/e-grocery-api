import geoalchemy2
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas

from .base import BaseCRUD


class RegionCRUD(BaseCRUD[models.Region, schemas.RegionCreate]):
    async def get_by_location(
        self,
        session: AsyncSession,
        geo_point: schemas.GeoPoint
    ) -> models.Region | None:

        return (await session.scalars(
            select(models.Region)
            .where(
                geoalchemy2.functions.ST_Covers(
                    models.Region._geo_polygon,
                    geoalchemy2.WKTElement(
                        f'POINT({geo_point.longitude} {geo_point.latitude})'
                    )
                )
            )
        )).first()


region = RegionCRUD(models.Region)
