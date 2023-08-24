import httpx
from fastapi import status

from src import models
from src.config import cfg_test
from src.main import app


async def test_create_item(
    client: httpx.AsyncClient,
    item_request_body: dict
) -> None:

    response = await client.post(
        app.url_path_for('create_item'),
        json=item_request_body
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body.keys() == cfg_test.ITEM_FIELDS


async def test_get_item_by_id(
    client: httpx.AsyncClient,
    db_item: models.Item
) -> None:

    response = await client.get(
        app.url_path_for('get_item_by_id', item_id=db_item.item_id)
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body = response.json()
    assert response_body.keys() == cfg_test.ITEM_FIELDS
