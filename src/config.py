import datetime as dt
import enum
import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class CourierType(str, enum.Enum):
    FOOT = 'FOOT', 3, 2, 10, 2
    BIKE = 'BIKE', 2, 3, 20, 4
    AUTO = 'AUTO', 1, 4, 40, 7

    rating_coeff: int
    earnings_coeff: int
    max_weight: int
    max_orders: int

    def __new__(
        cls, value, rating_coeff, earnings_coeff, max_weight, max_orders
    ):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.rating_coeff = rating_coeff
        obj.earnings_coeff = earnings_coeff
        obj.max_weight = max_weight
        obj.max_orders = max_orders
        return obj


class Settings(BaseSettings):

    API_V1_STR: str = '/api/v1'

    SECONDS_IN_HOUR: int = 3600

    SRID: int = 4326

    DEFAULT_LIMIT: int = 100
    DEFAULT_OFFSET: int = 0

    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30

    DB_DRIVER = os.getenv('DB_DRIVER')
    DB_DIALECT = os.getenv('DB_DIALECT')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    DB_URL: str = (
        f'{DB_DRIVER}+{DB_DIALECT}://{DB_USER}:{DB_PASS}'
        f'@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )

    class Config:
        case_sensitive = True


class TestSettings(BaseSettings):
    DB_DRIVER = os.getenv('DB_DRIVER')
    DB_DIALECT = os.getenv('DB_DIALECT')
    DB_USER = os.getenv('DB_USER_TEST')
    DB_PASS = os.getenv('DB_PASS_TEST')
    DB_HOST = os.getenv('DB_HOST_TEST')
    DB_PORT = os.getenv('DB_PORT_TEST')

    DB_URL: str = (
        f'{DB_DRIVER}+{DB_DIALECT}://{DB_USER}:{DB_PASS}@'
        f'{DB_HOST}:{DB_PORT}'
    )

    COURIER_START_AT: dt.datetime = dt.datetime(2023, 6, 6)
    COURIER_END_AT: dt.datetime = dt.datetime(2023, 6, 7)
    COURIER_RATING: float = 3.75
    COURIER_EARNINGS: int = 363_600
    DB_COURIERS_NUM: int = 21
    COURIER_FIELDS: set[str] = {
        'courier_id',
        'courier_type'
    }

    DB_ITEMS_NUM: int = 4
    ITEM_FIELDS: set[str] = {
        'item_id',
        'name',
        'weight',
        'price'
    }

    DB_ORDERS_NUM: int = 30
    ORDER_FIELDS: set[str] = {
        'order_id',
        'courier_id',
        'delivery_region_id',
        'delivery_address',
        'delivery_location',
        'created_at',
        'completed_at',
        'cost',
        'weight',
        'order_items'
    }

    DB_REGIONS_NUM: int = 4
    REGION_FIELDS: set[str] = {
        'region_id',
        'name',
        'geo_polygon'
    }

    DB_SHIFTS_NUM: int = 4
    SHIFT_FIELDS: set[str] = {
        'shift_id',
        'region_id',
        'date',
        'start_time',
        'end_time'
    }

    class Config:
        case_sensitive = True


cfg = Settings()
cfg_test = TestSettings()
