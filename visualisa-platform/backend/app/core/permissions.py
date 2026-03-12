"""
RBAC: Permission constants and dependency decorators
"""
from functools import wraps
from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.database import get_db
from app.models.user import User, UserRole


class Roles:
    SUPERADMIN = UserRole.SUPERADMIN
    ADMIN = UserRole.ADMIN
    PROFESSIONAL = UserRole.PROFESSIONAL


def require_roles(*roles: UserRole) -> Callable:
    """Dependency factory: require the current user to have one of the given roles."""
    async def _check_role(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise ForbiddenError("No tienes permisos para esta acción")
        return current_user
    return _check_role


def require_admin() -> Callable:
    return require_roles(UserRole.ADMIN, UserRole.SUPERADMIN)


def require_superadmin() -> Callable:
    return require_roles(UserRole.SUPERADMIN)


# Avoid circular import: get_current_user is defined in api/deps.py but we need it here.
# We import lazily below.
def get_current_user(db: AsyncSession = Depends(get_db)):  # type: ignore[empty-body]
    ...  # Real implementation in api/deps.py
