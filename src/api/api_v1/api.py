from fastapi import APIRouter

from src.api.api_v1.endpoints import couriers, items, orders, regions, shifts

api_router = APIRouter()
api_router.include_router(
    couriers.router,
    prefix='/couriers',
    tags=['couriers']
)
api_router.include_router(items.router, prefix='/items', tags=['items'])
api_router.include_router(orders.router, prefix='/orders', tags=['orders'])
api_router.include_router(regions.router, prefix='/regions', tags=['regions'])
api_router.include_router(shifts.router, prefix='/shifts', tags=['shifts'])
