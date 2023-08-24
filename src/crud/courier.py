from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas

from .base import BaseCRUD


class CourierCRUD(BaseCRUD[models.Courier, schemas.CourierCreate]):
    async def add_shift(
        self,
        session: AsyncSession,
        courier: models.Courier,
        shift: models.Shift
    ) -> models.Courier:

        courier.shifts.append(shift)

        return await self.add_commit_refresh(session, obj=courier)


courier = CourierCRUD(models.Courier)
