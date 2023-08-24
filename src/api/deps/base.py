from typing import Annotated, AsyncGenerator, Type

from fastapi import Depends, HTTPException, Request, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, database, models, schemas


async def get_session() -> AsyncGenerator[AsyncSession, None]:

    async with database.AsyncSessionLocal() as session:
        yield session


async def get_by_id_or_404(
    session: AsyncSession,
    *,
    model: Type[models.ModelType],
    object_id: UUID4
) -> models.ModelType:

    obj = await crud.BaseCRUD(model).get_by_id(session, object_id=object_id)

    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Object of {model} with id={object_id} not found.'
        )

    return obj


class GetByIdPathNameOr404:
    def __init__(
        self,
        model: Type[models.ModelType],
    ) -> None:
        self.model = model
        self.id_path_name: str = {
            models.Courier: 'courier_id',
            models.Item: 'item_id',
            models.Order: 'order_id',
            models.Region: 'region_id',
            models.Shift: 'shift_id'
        }[model]

    async def __call__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
        request: Request
    ) -> models.Base:

        object_id = request.path_params[self.id_path_name]

        try:
            UUID4(object_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f'Invalid {self.id_path_name}.'
            )

        return await get_by_id_or_404(
            session,
            model=self.model,
            object_id=object_id
        )


async def get_region_id_by_geo_point_or_400(
    session: AsyncSession,
    geo_point: schemas.GeoPoint
) -> UUID4:

    delivery_region = await crud.region.get_by_location(
        session,
        geo_point=geo_point
    )

    if delivery_region is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Unfortunately, we do not deliver to this address.'
        )

    return delivery_region.region_id
