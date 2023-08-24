import asyncio
import datetime as dt
from typing import AsyncGenerator

import httpx
import pytest
import yarl
from alembic.command import upgrade
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, database, models, schemas
from src.api.deps import get_session
from src.config import CourierType, cfg_test
from src.main import app

from . import utils


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def pg_url() -> yarl.URL:
    """
    Provides base PostgreSQL URL for creating temporary databases.
    """
    return yarl.URL(cfg_test.DB_URL)


@pytest.fixture(scope='session')
async def migrated_postgres_template(
    pg_url: yarl.URL
) -> AsyncGenerator[str, None]:
    """
    Creates temporary database and applies migrations.
    Database can be used as template to fast creation databases for tests.

    Has "session" scope, so is called only once per tests run.
    """
    async with utils.tmp_database(pg_url, 'template') as tmp_url:
        tmp_alembic_config = await utils.get_tmp_alembic_config_from_url(
            tmp_url
        )
        await utils.create_postgis_extension(tmp_url)
        upgrade(tmp_alembic_config, 'head')
        yield tmp_url


@pytest.fixture()
async def migrated_postgres(
    pg_url: yarl.URL,
    migrated_postgres_template: str
) -> AsyncGenerator[str, None]:
    """
    Quickly creates clean migrated database using temporary database as base.
    Use this fixture in tests that require migrated database.
    """
    template_db: str = yarl.URL(migrated_postgres_template).name
    async with utils.tmp_database(
        db_url=pg_url,
        suffix='pytest',
        template=template_db
    ) as tmp_url:
        yield tmp_url


@pytest.fixture()
async def session_test(
    migrated_postgres: str
) -> AsyncGenerator[AsyncSession, None]:

    _, TestAsyncSessionLocal = await database.get_engine_and_sessionmaker(
        migrated_postgres
    )
    async with TestAsyncSessionLocal() as session_test:
        yield session_test


@pytest.fixture()
async def courier_request_body() -> dict:

    return {'courier_type': CourierType.FOOT}


@pytest.fixture()
async def db_courier(
    session_test: AsyncSession,
    courier_request_body: dict
) -> models.Courier:

    return await crud.courier.create(
        session_test,
        object_in=schemas.CourierCreate(**courier_request_body)
    )


@pytest.fixture()
async def db_couriers(
    session_test: AsyncSession,
    courier_request_body: dict
) -> list[models.Courier]:

    return [
        await crud.courier.create(
            session_test,
            object_in=schemas.CourierCreate(**courier_request_body)
        )
        for _ in range(cfg_test.DB_COURIERS_NUM)
    ]


@pytest.fixture()
async def db_courier_with_shift(
    session_test: AsyncSession,
    db_courier: models.Courier,
    db_todays_shift: models.Shift
) -> models.Courier:

    return await crud.courier.add_shift(
        session_test,
        courier=db_courier,
        shift=db_todays_shift
    )


@pytest.fixture()
async def db_courier_with_completed_orders(
    session_test: AsyncSession,
    db_courier: models.Courier,
    completed_db_orders: list[models.Order]
) -> models.Courier:

    db_courier.orders.extend(completed_db_orders)

    return await crud.courier.add_commit_refresh(session_test, obj=db_courier)


@pytest.fixture()
async def item_request_body() -> dict:

    return {
        'name': 'cucumber',
        'weight': 1,
        'price': 101
    }


@pytest.fixture()
async def db_item(
    session_test: AsyncSession,
    item_request_body: dict
) -> models.Item:

    return await crud.item.create(
        session_test,
        object_in=schemas.ItemCreate(**item_request_body)
    )


@pytest.fixture()
async def order_request_body(db_item: models.Item) -> dict:

    DELIVERY_ADDRESS: str = 'ул.Лягушкина, д.22, кв.8'
    DELIVERY_LOCATION: dict[str, float] = {
        'latitude': 9.,
        'longitude': 0.
    }

    return {
        'delivery_address': DELIVERY_ADDRESS,
        'delivery_location': DELIVERY_LOCATION,
        'order_items': [
            {
                'item_id': str(db_item.item_id),
                'amount': 2
            }
        ]
    }


@pytest.fixture()
async def db_order(
    session_test: AsyncSession,
    db_region: models.Region,
    order_request_body: dict
) -> models.Order:

    order_request_body['delivery_region_id'] = str(db_region.region_id)

    return await crud.order.create(
        session_test,
        object_in=schemas.OrderCreate(**order_request_body)
    )


@pytest.fixture()
async def db_orders(
    session_test: AsyncSession,
    db_region: models.Region,
    order_request_body: dict
) -> list[models.Order]:

    order_request_body['delivery_region_id'] = str(db_region.region_id)

    return [
        await crud.order.create(
            session_test,
            object_in=schemas.OrderCreate(**order_request_body)
        )
        for _ in range(cfg_test.DB_ORDERS_NUM)
    ]


@pytest.fixture()
async def assigned_db_order(
    session_test: AsyncSession,
    db_order: models.Order,
    db_courier: models.Courier
) -> models.Order:

    return await crud.order.assign(
        session_test,
        order=db_order,
        courier=db_courier
    )


@pytest.fixture()
async def completed_db_orders(
    session_test: AsyncSession,
    db_orders: list[models.Order],
    order_request_body: dict
) -> list[models.Order]:

    return [
        await crud.order.complete(
            session_test,
            order=order,
            completed_at=cfg_test.COURIER_START_AT
        )
        for order in db_orders
    ]


@pytest.fixture()
async def region_request_body() -> dict:

    REGION_NAME = 'Океан'
    REGION_GEO_POLYGON = [
        {
            'latitude': -10.,
            'longitude': 0.
        },
        {
            'latitude': 10.,
            'longitude': 10.
        },
        {
            'latitude': 10.,
            'longitude': -10.
        },
        {
            'latitude': -10.,
            'longitude': 0.
        }
    ]

    return {
        'name': REGION_NAME,
        'geo_polygon': REGION_GEO_POLYGON
    }


@pytest.fixture()
async def db_region(
    session_test: AsyncSession,
    region_request_body
) -> models.Region:

    return await crud.region.create(
        session_test,
        object_in=schemas.RegionCreate(**region_request_body)
    )


@pytest.fixture()
async def shift_request_body(db_region: models.Region) -> dict:

    return {
        'region_id': str(db_region.region_id),
        'date': str(dt.datetime.utcnow().date()),
        'start_time': str(dt.time(0)),
        'end_time': str(dt.time(23, 59, 59))
    }


@pytest.fixture()
async def db_todays_shift(
    session_test: AsyncSession,
    shift_request_body: dict
) -> models.Shift:

    return await crud.shift.create(
        session_test,
        object_in=schemas.ShiftCreate(**shift_request_body)
    )


@pytest.fixture()
async def client(
    session_test: AsyncSession
) -> AsyncGenerator[httpx.AsyncClient, None]:

    async def _get_test_session():
        return session_test

    app.dependency_overrides[get_session] = _get_test_session
    async with httpx.AsyncClient(app=app, base_url='http://test') as client:
        yield client
