"""
Visualisa Platform — FastAPI Application Factory
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config import settings
from app.database import engine, Base
from app.api.v1.router import api_router
from app.api.public.router import public_router
from app.core.middleware import RateLimitMiddleware, RequestLoggingMiddleware
from app.core.exceptions import register_exception_handlers

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: startup and shutdown events."""
    logger.info("Starting Visualisa Platform", version=settings.APP_VERSION)
    # Create all tables (in dev; prod uses Alembic migrations)
    if settings.ENV == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("Shutting down Visualisa Platform")
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Visualisa Platform API",
        description="AI-powered renovation visualizer for Dominican Republic real estate",
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.ENV != "production" else None,
        redoc_url="/redoc" if settings.ENV != "production" else None,
        lifespan=lifespan,
    )

    # --- Middleware ---
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)

    # --- Exception handlers ---
    register_exception_handlers(app)

    # --- Routers ---
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(public_router, prefix="/public")

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok", "version": settings.APP_VERSION}

    return app


app = create_app()
