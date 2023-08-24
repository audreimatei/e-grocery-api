import datetime as dt
from typing import Annotated

import numpy as np
from fastapi import Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas

from .base import (
    GetByIdPathNameOr404,
    get_by_id_or_404,
    get_region_id_by_geo_point_or_400,
    get_session
)


async def get_valid_creation_order_schema(
    session: Annotated[AsyncSession, Depends(get_session)],
    order_in: schemas.OrderCreate
) -> schemas.OrderCreate:

    unique_items_ids, counts = np.unique(
        np.array([order_item.item_id for order_item in order_in.order_items]),
        return_counts=True
    )
    duplicate_items_ids = list(unique_items_ids[counts > 1])
    if duplicate_items_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f'Items with ids={duplicate_items_ids}'
                ' are added multiple times.'
            )
        )

    for order_item in order_in.order_items:
        await get_by_id_or_404(
            session,
            model=models.Item,
            object_id=order_item.item_id
        )

    order_in.delivery_region_id = await get_region_id_by_geo_point_or_400(
        session,
        order_in.delivery_location
    )

    return order_in


async def get_valid_assignment_order(
    order: Annotated[models.Order, Depends(GetByIdPathNameOr404(models.Order))]
) -> models.Order:
    """
    Check that order has not been completed or assigned.

    Args:
        order: order for which we want to assign a courier.

    Returns:
        order: order ready for assignment to a courier.

    Raises:
        fastapi.HTTPException
    """
    if order.completed_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Order with id={order.order_id} has been completed.'
        )

    if order.courier_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Order with id={order.order_id} has been assigned'
        )

    return order


async def get_valid_assignment_couriers(
    session: Annotated[AsyncSession, Depends(get_session)],
    order: Annotated[models.Order, Depends(get_valid_assignment_order)]
) -> list[models.Courier]:
    """
    Find couriers who can take the order.
    Algorithm:
        1) In the order region, select today's shifts that haven't ended yet
           and have couriers, ordered by start time.
        2) Find first shift that has couriers available to pick up the order.
        3) Return couriers from this shift.

    Args:
        session: sqlalchemy.ext.asyncio AsyncSession object.
        order: order ready for assignment to a courier.

    Returns:
        assignment_couriers: couriers who can take the order.

    Raises:
        fastapi.HTTPException
    """
    todays_shifts_ordered_by_start_time = await crud.shift.get_for_order(
        session,
        order=order
    )

    if not todays_shifts_ordered_by_start_time:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No shifts found in order region for today.'
        )

    for shift in todays_shifts_ordered_by_start_time:
        assignment_couriers = [
            courier
            for courier in shift.couriers
            if courier.weight + order.weight <= courier.courier_type.max_weight
            and len(courier.orders) + 1 <= courier.courier_type.max_orders
        ]

        if assignment_couriers:
            return assignment_couriers

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='No available assignment couriers found for todays shifts'
    )


async def get_valid_completion_order(
    session: Annotated[AsyncSession, Depends(get_session)],
    completed_at: Annotated[dt.datetime, Body(embed=True)],
    order: Annotated[models.Order, Depends(GetByIdPathNameOr404(models.Order))]
) -> models.Order:

    if order.courier_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Order with id={order.order_id} is not assigned.'
        )
    elif (
        order.completed_at is not None
        and order.completed_at != completed_at
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f'Order with id={order.order_id}'
                ' already completed with a different time.'
            )
        )

    return order
