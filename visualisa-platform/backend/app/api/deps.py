"""
API Dependencies: database session, current user, admin guard, pro guard
"""
import uuid

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_token
from app.database import get_db
from app.models.professional import ProfessionalProfile
from app.models.user import User, UserRole

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials:
        raise UnauthorizedError("Token de autenticación requerido")
    try:
        payload = decode_token(credentials.credentials)
        user_id: str = payload["sub"]
        token_type: str = payload.get("type", "")
        if token_type != "access":
            raise UnauthorizedError("Token de acceso inválido")
    except (JWTError, KeyError):
        raise UnauthorizedError("Token inválido o expirado")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise UnauthorizedError("Usuario no encontrado o desactivado")
    return user


async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if user.role not in (UserRole.ADMIN, UserRole.SUPERADMIN):
        raise ForbiddenError()
    return user


async def get_current_superadmin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.SUPERADMIN:
        raise ForbiddenError()
    return user


async def get_current_professional(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> tuple[User, ProfessionalProfile]:
    if user.role != UserRole.PROFESSIONAL:
        raise ForbiddenError("Solo profesionales pueden acceder a este recurso")
    result = await db.execute(
        select(ProfessionalProfile).where(ProfessionalProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Perfil profesional no configurado. Completa el onboarding.",
        )
    return user, profile


async def get_widget_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: AsyncSession = Depends(get_db),
) -> ProfessionalProfile:
    """Authenticate widget requests by API key from X-API-Key header."""
    if not x_api_key:
        raise UnauthorizedError("API key requerida")
    result = await db.execute(
        select(ProfessionalProfile).where(ProfessionalProfile.api_key == x_api_key)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise UnauthorizedError("API key inválida")
    return profile
