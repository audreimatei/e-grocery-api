import datetime as dt

import httpx
from fastapi import status

from src import models
from src.config import cfg, cfg_test
from src.main import app


async def test_create_order(
    client: httpx.AsyncClient,
    db_region: models.Region,
    order_request_body: dict
) -> None:

    response = await client.post(
        app.url_path_for('create_order'),
        json=order_request_body
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body.keys() == cfg_test.ORDER_FIELDS


async def test_assign_order(
    client: httpx.AsyncClient,
    db_courier_with_shift: models.Courier,
    db_order: models.Order
) -> None:

    response = await client.post(
        app.url_path_for('assign_order', order_id=db_order.order_id)
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body.keys() == cfg_test.ORDER_FIELDS


async def test_get_orders(
    client: httpx.AsyncClient,
    db_orders: list[models.Order]
) -> None:

    limit = cfg.DEFAULT_LIMIT
    offset = cfg.DEFAULT_OFFSET

    response = await client.get(app.url_path_for('get_orders'))
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body['limit'] == limit
    assert response_body['offset'] == offset

    db_orders_lo = db_orders[offset:offset+limit]
    assert len(db_orders_lo) == len(response_body['orders'])

    for res_order in response_body['orders']:
        assert res_order.keys() == cfg_test.ORDER_FIELDS


async def test_get_order_by_id(
    client: httpx.AsyncClient,
    db_order: models.Order
) -> None:

    response = await client.get(
        app.url_path_for('get_order_by_id', order_id=db_order.order_id)
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body = response.json()
    assert response_body.keys() == cfg_test.ORDER_FIELDS


async def test_complete_order_by_id(
    client: httpx.AsyncClient,
    assigned_db_order: models.Order
) -> None:

    response = await client.post(
        app.url_path_for(
            'complete_order_by_id',
            order_id=assigned_db_order.order_id
        ),
        json={'completed_at': str(dt.datetime.utcnow())}
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body.keys() == cfg_test.ORDER_FIELDS
    assert assigned_db_order.completed_at == (
        dt.datetime.fromisoformat(response_body['completed_at'])
    )
