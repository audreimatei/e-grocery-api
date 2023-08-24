from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps
from src.config import cfg

router = APIRouter()


@router.post('/', response_model=schemas.Region)
async def create_region(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    region_in: schemas.RegionCreate
):
    return await crud.region.create(session, object_in=region_in)


@router.get('/', response_model=schemas.RegionsLimitOffset)
async def get_regions(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    limit: Annotated[int, Query(ge=1)] = cfg.DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=0)] = cfg.DEFAULT_OFFSET
):
    return {
        'regions': await crud.region.get(session, limit=limit, offset=offset),
        'limit': limit,
        'offset': offset
    }


@router.get('/{region_id}/', response_model=schemas.Region)
async def get_region_by_id(
    region_id: UUID4,
    region: Annotated[
        models.Courier,
        Depends(deps.GetByIdPathNameOr404(models.Region))
    ]
):
    return region
