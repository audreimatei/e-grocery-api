import os
import uuid
from argparse import Namespace
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import AsyncGenerator

import sqlalchemy_utils
import yarl
from alembic.config import Config
from sqlalchemy.sql import text

from src import database

PROJECT_PATH = str(Path(__file__).parent.parent.resolve())


async def make_tmp_alembic_config(
    cmd_opts: Namespace,
    base_path: str = PROJECT_PATH
) -> Config:
    # Replace path to alembic.ini file to absolute
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(
        file_=cmd_opts.config,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts
    )

    # Replace path to alembic folder to absolute
    alembic_location = config.get_main_option('script_location')
    if alembic_location is not None and not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))
    if cmd_opts.pg_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.pg_url)

    return config


async def get_tmp_alembic_config_from_url(pg_url: str | None = None) -> Config:
    """
    Provides Python object, representing alembic.ini file.
    """
    cmd_options = SimpleNamespace(
        config='alembic.ini', name='alembic', pg_url=pg_url,
        raiseerr=False, x=None,
    )

    return await make_tmp_alembic_config(cmd_options)  # type: ignore


@asynccontextmanager
async def tmp_database(
    db_url: yarl.URL,
    suffix: str = '',
    **kwargs
) -> AsyncGenerator[str, None]:

    tmp_db_name: str = '.'.join([uuid.uuid4().hex, suffix])
    tmp_db_url: str = str(db_url.with_path(tmp_db_name))
    sqlalchemy_utils.create_database(tmp_db_url, **kwargs)

    try:
        yield tmp_db_url
    finally:
        sqlalchemy_utils.drop_database(tmp_db_url)


async def create_postgis_extension(db_url: str) -> None:

    async_engine, _ = await database.get_engine_and_sessionmaker(db_url)
    async with async_engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS postgis;'))
    await async_engine.dispose()
