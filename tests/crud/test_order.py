import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models
from src.config import cfg


async def test_crud_create_order(db_order: models.Order) -> None:

    assert db_order.order_id
    assert db_order.courier_id is None
    assert db_order.delivery_region_id
    assert db_order.delivery_address
    assert db_order.delivery_location
    assert db_order.created_at
    assert db_order.completed_at is None
    assert db_order.cost
    assert db_order.weight
    assert db_order.order_items


async def test_crud_assign_order(
    session_test: AsyncSession,
    db_order: models.Order,
    db_courier: models.Courier
) -> None:

    assert db_order.courier_id is None

    await crud.order.assign(session_test, order=db_order, courier=db_courier)

    assert db_order.courier_id == db_courier.courier_id
    assert db_order in db_courier.orders


async def test_crud_get_orders(
    session_test: AsyncSession,
    db_orders: list[models.Order]
) -> None:

    limit = cfg.DEFAULT_LIMIT
    offset = cfg.DEFAULT_OFFSET

    db_orders_2 = await crud.order.get(
        session_test,
        limit=limit,
        offset=offset
    )
    assert db_orders[offset:offset+limit] == db_orders_2


async def test_crud_get_order_by_id(
    session_test: AsyncSession,
    db_order: models.Order
) -> None:

    db_order_2 = await crud.order.get_by_id(
        session_test,
        object_id=db_order.order_id
    )
    assert db_order == db_order_2


async def test_crud_complete_order_by_id(
    session_test: AsyncSession,
    assigned_db_order: models.Order
) -> None:

    assert assigned_db_order.completed_at is None

    utc_now = dt.datetime.utcnow()
    await crud.order.complete(
        session_test,
        order=assigned_db_order,
        completed_at=utc_now
    )
    assert assigned_db_order.completed_at == utc_now
