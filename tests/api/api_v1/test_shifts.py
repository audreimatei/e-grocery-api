import httpx
from fastapi import status

from src import models
from src.config import cfg_test
from src.main import app


async def test_create_shift(
    client: httpx.AsyncClient,
    shift_request_body: dict
) -> None:

    response = await client.post(
        app.url_path_for('create_shift'),
        json=shift_request_body
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body.keys() == cfg_test.SHIFT_FIELDS


async def test_get_shift_by_id(
    client: httpx.AsyncClient,
    db_todays_shift: models.shift
) -> None:

    response = await client.get(
        app.url_path_for('get_shift_by_id', shift_id=db_todays_shift.shift_id)
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body = response.json()
    assert response_body.keys() == cfg_test.SHIFT_FIELDS
