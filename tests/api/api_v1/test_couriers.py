import httpx
from fastapi import status

from src import models
from src.config import cfg, cfg_test
from src.main import app


async def test_create_courier(
    client: httpx.AsyncClient,
    courier_request_body: dict
) -> None:

    response = await client.post(
        app.url_path_for('create_courier'),
        json=courier_request_body
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body.keys() == cfg_test.COURIER_FIELDS


async def test_add_shift_to_courier(
    client: httpx.AsyncClient,
    db_courier: models.Courier,
    db_todays_shift: models.Shift
) -> None:

    response = await client.post(
        app.url_path_for(
            'add_shift_to_courier',
            courier_id=db_courier.courier_id,
            shift_id=db_todays_shift.shift_id
        )
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body.keys() == cfg_test.COURIER_FIELDS


async def test_get_couriers(
    client: httpx.AsyncClient,
    db_couriers: list[models.Courier]
) -> None:

    limit = cfg.DEFAULT_LIMIT
    offset = cfg.DEFAULT_OFFSET

    response = await client.get(app.url_path_for('get_couriers'))
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body['limit'] == limit
    assert response_body['offset'] == offset

    db_couriers_lo = db_couriers[offset:offset+limit]
    assert len(db_couriers_lo) == len(response_body['couriers'])

    for res_courier in response_body['couriers']:
        assert res_courier.keys() == cfg_test.COURIER_FIELDS


async def test_get_courier_by_id(
    client: httpx.AsyncClient,
    db_courier: models.Courier
) -> None:

    response = await client.get(
        app.url_path_for('get_courier_by_id', courier_id=db_courier.courier_id)
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    res_courier = response.json()
    assert res_courier.keys() == cfg_test.COURIER_FIELDS


async def test_get_courier_meta_info_by_id(
    client: httpx.AsyncClient,
    db_courier_with_completed_orders: models.Courier
) -> None:

    response = await client.get(
        app.url_path_for(
            'get_courier_meta_info_by_id',
            courier_id=db_courier_with_completed_orders.courier_id
        ),
        params={
            'start_at': str(cfg_test.COURIER_START_AT),
            'end_at': str(cfg_test.COURIER_END_AT)
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body = response.json()
    assert response_body.keys() == {'rating', 'earnings'}
