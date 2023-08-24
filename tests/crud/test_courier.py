from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models
from src.config import cfg


async def test_crud_create_courier(db_courier: models.Courier) -> None:

    assert db_courier.courier_id
    assert db_courier.courier_type


async def test_crud_add_shift_to_courier(
    session_test: AsyncSession,
    db_courier: models.Courier,
    db_todays_shift: models.Shift
) -> None:

    assert db_todays_shift not in db_courier.shifts

    await crud.courier.add_shift(
        session_test,
        courier=db_courier,
        shift=db_todays_shift
    )
    assert db_todays_shift in db_courier.shifts


async def test_crud_get_couriers(
    session_test: AsyncSession,
    db_couriers: list[models.Courier]
) -> None:

    limit = cfg.DEFAULT_LIMIT
    offset = cfg.DEFAULT_OFFSET

    db_couriers_2 = await crud.courier.get(
        session_test,
        limit=limit,
        offset=offset
    )
    assert db_couriers[offset:offset+limit] == db_couriers_2


async def test_crud_get_courier_by_id(
    session_test: AsyncSession,
    db_courier: models.Courier
) -> None:

    db_courier_2 = await crud.courier.get_by_id(
        session_test,
        object_id=db_courier.courier_id
    )
    assert db_courier == db_courier_2
