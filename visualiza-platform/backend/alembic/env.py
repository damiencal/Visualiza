"""Alembic environment configuration.

Supports async SQLAlchemy engines (aiomysql) via run_async_migrations helper,
and sync engines (pymysql) for the legacy ``--sql`` offline mode.
"""
from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# ── Import app config & declarative Base ────────────────────────────────────
import sys
import os

# Make sure the `app` package is importable when running alembic from the
# backend/ directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import settings  # noqa: E402
from app.models.base import Base  # noqa: E402
# Import every model so metadata is fully populated
from app.models import (  # noqa: F401, E402
    user,
    professional,
    product,
    crawler,
    bom,
    billing,
    visualizer,
)

# ── Alembic config object ────────────────────────────────────────────────────
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use sync URL for Alembic (aiomysql ↔ pymysql)
sync_url = settings.SYNC_DATABASE_URL
config.set_main_option("sqlalchemy.url", sync_url)

target_metadata = Base.metadata


# ── Offline migrations (emit pure SQL) ──────────────────────────────────────
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Online migrations (async) ────────────────────────────────────────────────
def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        # async_engine_from_config doesn't accept pymysql URL — swap dialect
        {"sqlalchemy.url": settings.DATABASE_URL, "sqlalchemy.poolclass": pool.NullPool},
        prefix="sqlalchemy.",
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
