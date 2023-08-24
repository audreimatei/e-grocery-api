from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps
from src.config import cfg

router = APIRouter()


@router.post('/', response_model=schemas.Shift)
async def create_shift(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    shift_in: schemas.ShiftCreate
):
    return await crud.shift.create(session, object_in=shift_in)


@router.get('/', response_model=schemas.ShiftsLimitOffset)
async def get_shifts(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    limit: Annotated[int, Query(ge=1)] = cfg.DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=0)] = cfg.DEFAULT_OFFSET
):
    return {
        'shifts': await crud.shift.get(session, limit=limit, offset=offset),
        'limit': limit,
        'offset': offset
    }


@router.get('/{shift_id}/', response_model=schemas.Shift)
async def get_shift_by_id(
    shift_id: UUID4,
    shift: Annotated[
        models.Shift,
        Depends(deps.GetByIdPathNameOr404(models.Shift))
    ]
):
    return shift
