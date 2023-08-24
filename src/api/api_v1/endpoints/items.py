from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps
from src.config import cfg

router = APIRouter()


@router.post('/', response_model=schemas.Item)
async def create_item(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    item_in: Annotated[
        schemas.ItemCreate,
        Depends(deps.get_valid_creation_item_schema)
    ]
):
    return await crud.item.create(session, object_in=item_in)


@router.get('/', response_model=schemas.ItemsLimitOffset)
async def get_items(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    limit: Annotated[int, Query(ge=1)] = cfg.DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=0)] = cfg.DEFAULT_OFFSET
):
    return {
        'items': await crud.item.get(session, limit=limit, offset=offset),
        'limit': limit,
        'offset': offset
    }


@router.get('/{item_id}/', response_model=schemas.Item)
async def get_item_by_id(
    item_id: UUID4,
    item: Annotated[
        models.Courier,
        Depends(deps.GetByIdPathNameOr404(models.Item))
    ]
):
    return item
