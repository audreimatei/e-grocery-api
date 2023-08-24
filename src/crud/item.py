from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas

from .base import BaseCRUD


class ItemCRUD(BaseCRUD[models.Item, schemas.ItemCreate]):
    async def get_by_name(
        self,
        session: AsyncSession,
        *,
        name: str
    ) -> models.Item | None:

        return (await session.scalars(
            select(models.Item)
            .where(models.Item.name == name)
        )).one_or_none()


item = ItemCRUD(models.Item)
