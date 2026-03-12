"""
Pytest configuration and shared fixtures.

Uses an in-memory SQLite database to avoid needing a running MariaDB instance
during tests.  The async SQLAlchemy engine is swapped via FastAPI dependency
overrides so the real `app.database.get_db` is never called.
"""
from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.api.deps import get_db
from app.models.base import Base
from app.core.security import create_access_token, get_password_hash
from app.models.user import User, UserRole

# ── In-memory SQLite async engine ────────────────────────────────────────────

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


# ── Event-loop – one loop per session (faster) ───────────────────────────────

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ── Database lifecycle ───────────────────────────────────────────────────────

@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    """Create all tables once per test session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a fresh DB session per test, rolling back afterwards."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


# ── Dependency override ───────────────────────────────────────────────────────

@pytest_asyncio.fixture(autouse=True)
async def override_db(db: AsyncSession):
    async def _get_test_db():
        yield db

    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.pop(get_db, None)


# ── HTTP client ──────────────────────────────────────────────────────────────

@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


# ── User fixtures ─────────────────────────────────────────────────────────────

@pytest_asyncio.fixture()
async def admin_user(db: AsyncSession) -> User:
    user = User(
        email="testadmin@visualisa.web.do",
        hashed_password=get_password_hash("Admin1234!"),
        full_name="Test Admin",
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    await db.flush()
    return user


@pytest_asyncio.fixture()
async def admin_headers(admin_user: User) -> dict[str, str]:
    token = create_access_token(subject=str(admin_user.id))
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture()
async def pro_user(db: AsyncSession) -> User:
    user = User(
        email="testpro@visualisa.web.do",
        hashed_password=get_password_hash("Pro1234!"),
        full_name="Test Professional",
        role=UserRole.PROFESSIONAL,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    await db.flush()
    return user


@pytest_asyncio.fixture()
async def pro_headers(pro_user: User) -> dict[str, str]:
    token = create_access_token(subject=str(pro_user.id))
    return {"Authorization": f"Bearer {token}"}
