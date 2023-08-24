from typing import Annotated, TypeVar

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


CreateSchemaType = TypeVar('CreateSchemaType', bound=ORJSONModel)


class GeoPoint(ORJSONModel):
    latitude: Annotated[float, Field(ge=-90., le=90.)]
    longitude: Annotated[float, Field(ge=-180., le=180.)]
