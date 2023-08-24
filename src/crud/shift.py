from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas

from .base import BaseCRUD


class ShiftCRUD(BaseCRUD[models.Shift, schemas.ShiftCreate]):
    async def get_for_order(
        self,
        session: AsyncSession,
        *,
        order: models.Order
    ) -> list[models.Shift]:

        return list((await session.scalars(
            select(models.Shift)
            .where(
                and_(
                    models.Shift.region_id == order.delivery_region_id,
                    models.Shift.date == order.created_at.date(),
                    models.Shift.end_time > order.created_at.time(),
                    models.Shift.couriers
                )
            )
            .order_by(models.Shift.start_time)
        )).all())


shift = ShiftCRUD(models.Shift)
