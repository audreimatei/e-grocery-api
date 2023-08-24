import asyncio
import logging

import tenacity
from sqlalchemy import text

from src import database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 2


@tenacity.retry(
    stop=tenacity.stop_after_attempt(max_tries),
    wait=tenacity.wait_fixed(wait_seconds),
    before=tenacity.before_log(logger, logging.INFO),
    after=tenacity.after_log(logger, logging.WARN),
)
async def init() -> None:
    try:
        # Try to create connection to check if DB is awake
        async with database.async_engine.begin() as conn:
            await conn.execute(text('SELECT 1'))
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info('Initializing service')
    await init()
    logger.info('Service finished initializing')


if __name__ == '__main__':
    asyncio.run(main())
