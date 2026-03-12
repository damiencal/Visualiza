"""
Custom HTTP exceptions and centralized registration
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from jose import JWTError


class VisualizaException(Exception):
    def __init__(self, status_code: int, detail: str, code: str | None = None) -> None:
        self.status_code = status_code
        self.detail = detail
        self.code = code
        super().__init__(detail)


class NotFoundError(VisualizaException):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, f"{resource} no encontrado")


class UnauthorizedError(VisualizaException):
    def __init__(self, detail: str = "No autorizado") -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, "unauthorized")


class ForbiddenError(VisualizaException):
    def __init__(self, detail: str = "Acceso denegado") -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail, "forbidden")


class ConflictError(VisualizaException):
    def __init__(self, detail: str = "Recurso ya existe") -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail, "conflict")


class RateLimitError(VisualizaException):
    def __init__(self, detail: str = "Límite de solicitudes alcanzado") -> None:
        super().__init__(status.HTTP_429_TOO_MANY_REQUESTS, detail, "rate_limit")


class PlanLimitError(VisualizaException):
    def __init__(self, detail: str = "Límite del plan alcanzado. Por favor actualiza tu plan.") -> None:
        super().__init__(status.HTTP_402_PAYMENT_REQUIRED, detail, "plan_limit")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(VisualizaException)
    async def visualiza_exception_handler(
        request: Request, exc: VisualizaException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "code": exc.code},
        )

    @app.exception_handler(JWTError)
    async def jwt_exception_handler(request: Request, exc: JWTError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token inválido o expirado", "code": "invalid_token"},
        )
