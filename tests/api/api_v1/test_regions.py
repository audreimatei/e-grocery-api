import httpx
from fastapi import status

from src import models
from src.config import cfg_test
from src.main import app


async def test_create_region(
    client: httpx.AsyncClient,
    region_request_body: dict
) -> None:

    response = await client.post(
        app.url_path_for('create_region'),
        json=region_request_body
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body: dict = response.json()
    assert response_body.keys() == cfg_test.REGION_FIELDS


async def test_get_region_by_id(
    client: httpx.AsyncClient,
    db_region: models.Region
) -> None:

    response = await client.get(
        app.url_path_for('get_region_by_id', region_id=db_region.region_id)
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response_body = response.json()
    assert response_body.keys() == cfg_test.REGION_FIELDS
