from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas

from .base import get_session


async def get_valid_creation_item_schema(
    session: Annotated[AsyncSession, Depends(get_session)],
    item_in: schemas.ItemCreate
) -> schemas.ItemCreate:

    if await crud.item.get_by_name(session, name=item_in.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f'Item with name="{item_in.name}" already exists.'
                'The name must be unique.'
            )
        )

    return item_in
