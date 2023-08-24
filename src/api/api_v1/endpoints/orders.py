import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, logic, models, schemas
from src.api import deps
from src.config import cfg

router = APIRouter()


@router.post('/', response_model=schemas.Order)
async def create_order(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    order_in: Annotated[
        schemas.OrderCreate,
        Depends(deps.get_valid_creation_order_schema)
    ]
):
    return await crud.order.create(session, object_in=order_in)


@router.post('/{order_id}/courier/', response_model=schemas.Order)
async def assign_order(
    order_id: UUID4,
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    assignment_order: Annotated[
        models.Order,
        Depends(deps.get_valid_assignment_order)
    ],
    assignment_couriers: Annotated[
        list[models.Courier],
        Depends(deps.get_valid_assignment_couriers)
    ]
):
    assignment_courier = await logic.courier.get_optimal_for_order(
        order=assignment_order,
        couriers=assignment_couriers
    )

    return await crud.order.assign(
        session,
        order=assignment_order,
        courier=assignment_courier
    )


@router.get('/', response_model=schemas.OrdersLimitOffset)
async def get_orders(
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    limit: Annotated[int, Query(ge=1)] = cfg.DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=0)] = cfg.DEFAULT_OFFSET
):
    return {
        'orders': await crud.order.get(session, limit=limit, offset=offset),
        'limit': limit,
        'offset': offset
    }


@router.get('/{order_id}/', response_model=schemas.Order)
async def get_order_by_id(
    order_id: UUID4,
    order: Annotated[
        models.Order,
        Depends(deps.GetByIdPathNameOr404(models.Order))
    ],
):
    return order


@router.post('/{order_id}/completed_at/', response_model=schemas.Order)
async def complete_order_by_id(
    order_id: UUID4,
    session: Annotated[AsyncSession, Depends(deps.get_session)],
    completed_at: Annotated[dt.datetime, Body(embed=True)],
    order: Annotated[models.Order, Depends(deps.get_valid_completion_order)]
):
    return await crud.order.complete(
        session,
        completed_at=completed_at,
        order=order
    )
