from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.api.api_v1.api import api_router
from src.config import cfg

app = FastAPI(
    title='e-grocery-api', 
    openapi_url=f'{cfg.API_V1_STR}/openapi.json'
)

limiter = Limiter(key_func=get_remote_address, default_limits=['100/second'])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(api_router, prefix=cfg.API_V1_STR)
