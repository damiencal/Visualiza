"""
Middleware: request logging, rate limiting
"""
import time
from collections import defaultdict
from typing import Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)

# Simple in-memory rate limiter (production: use Redis sliding window)
_request_counts: dict[str, list[float]] = defaultdict(list)
RATE_WINDOW_SECONDS = 60


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Global rate limiter: 60 req/min per IP for general API.
    Widget/public endpoints use per-key Redis-based limiting in their own handlers.
    """

    RATE_LIMIT = 120  # req/min for authenticated API
    PUBLIC_RATE_LIMIT = 30  # req/min for unauthenticated

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - RATE_WINDOW_SECONDS

        timestamps = _request_counts[client_ip]
        # Purge old entries
        _request_counts[client_ip] = [t for t in timestamps if t > window_start]
        _request_counts[client_ip].append(now)

        limit = (
            self.PUBLIC_RATE_LIMIT
            if request.url.path.startswith("/public")
            else self.RATE_LIMIT
        )

        if len(_request_counts[client_ip]) > limit:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=429,
                content={"detail": "Límite de solicitudes alcanzado", "code": "rate_limit"},
                headers={"Retry-After": "60"},
            )

        return await call_next(request)
