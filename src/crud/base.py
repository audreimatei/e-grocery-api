from typing import Generic, Type

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import class_mapper

from src import models, schemas


class BaseCRUD(Generic[models.ModelType, schemas.CreateSchemaType]):
    def __init__(self, model: Type[models.ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete.

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def add_commit_refresh(
        self,
        session: AsyncSession,
        *,
        obj: models.ModelType
    ) -> models.ModelType:

        session.add(obj)
        await session.commit()
        await session.refresh(obj)

        return obj

    async def create(
        self,
        session: AsyncSession,
        *,
        object_in: schemas.CreateSchemaType
    ) -> models.ModelType:

        return await self.add_commit_refresh(
            session,
            obj=self.model(**dict(object_in))
        )

    async def get(
        self,
        session: AsyncSession,
        *,
        limit: int,
        offset: int,
    ) -> list[models.ModelType]:

        return list((await session.scalars(
            select(self.model)
            .limit(limit)
            .offset(offset)
        )).all())

    async def get_by_id(
        self,
        session: AsyncSession,
        *,
        object_id: UUID4
    ) -> models.ModelType | None:

        return (await session.scalars(
            select(self.model)
            .where(class_mapper(self.model).primary_key[0] == object_id)
        )).one_or_none()
