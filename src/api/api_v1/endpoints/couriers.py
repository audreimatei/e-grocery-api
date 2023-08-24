import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, logic, models, schemas
from src.api import deps
from src.config import cfg

router = APIRouter()


@router.post('/', response_model=schemas.Courier)
async def create_courier(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    courier_in: schemas.CourierCreate
):
    return await crud.courier.create(session, object_in=courier_in)


@router.post(
    '/{courier_id}/shifts/{shift_id}/',
    response_model=schemas.Courier
)
async def add_shift_to_courier(
    courier_id: UUID4,
    shift_id: UUID4,
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    courier: Annotated[
        models.Courier,
        Depends(deps.GetByIdPathNameOr404(models.Courier))
    ],
    shift: Annotated[models.Shift, Depends(deps.get_valid_shift_to_add)]
):
    return await crud.courier.add_shift(session, courier=courier, shift=shift)


@router.get('/', response_model=schemas.CouriersLimitOffset)
async def get_couriers(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    limit: Annotated[int, Query(ge=1)] = cfg.DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=0)] = cfg.DEFAULT_OFFSET
):
    return {
        'couriers': await crud.courier.get(
            session,
            limit=limit,
            offset=offset
        ),
        'limit': limit,
        'offset': offset
    }


@router.get('/{courier_id}/', response_model=schemas.Courier)
async def get_courier_by_id(
    courier_id: UUID4,
    courier: Annotated[
        models.Courier,
        Depends(deps.GetByIdPathNameOr404(models.Courier))
    ]
):
    return courier


@router.get('/{courier_id}/meta-info/', response_model=schemas.CourierMetaInfo)
async def get_courier_meta_info_by_id(
    courier_id: UUID4,
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    start_at: Annotated[dt.datetime, Query()],
    end_at: Annotated[dt.datetime, Query()],
    courier: Annotated[
        models.Courier,
        Depends(deps.GetByIdPathNameOr404(models.Courier))
    ]
):
    return {
        'rating': await logic.courier.get_rating(courier, start_at, end_at),
        'earnings': await logic.courier.get_earnings(courier, start_at, end_at)
    }
