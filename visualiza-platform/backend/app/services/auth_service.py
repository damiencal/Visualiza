"""
Auth service: register, login, refresh, password reset
"""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token, create_refresh_token, decode_token,
    generate_api_key, generate_password_reset_token, hash_password,
    verify_password, verify_password_reset_token,
)
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest, TokenResponse


class AuthService:
    @staticmethod
    async def register(data: RegisterRequest, db: AsyncSession) -> User:
        existing = await db.execute(select(User).where(User.email == data.email))
        if existing.scalar_one_or_none():
            raise ConflictError("El correo ya está registrado")

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            phone=data.phone,
            role=UserRole.PROFESSIONAL,
        )
        db.add(user)
        await db.flush()
        return user

    @staticmethod
    async def login(email: str, password: str, db: AsyncSession) -> TokenResponse:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Credenciales incorrectas")
        if not user.is_active:
            raise UnauthorizedError("Cuenta desactivada")

        return TokenResponse(
            access_token=create_access_token(str(user.id), user.role.value),
            refresh_token=create_refresh_token(str(user.id)),
            expires_in=1800,
        )

    @staticmethod
    async def refresh(refresh_token: str, db: AsyncSession) -> TokenResponse:
        from jose import JWTError
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise UnauthorizedError()
        except JWTError:
            raise UnauthorizedError("Token de refresco inválido")

        result = await db.execute(select(User).where(User.id == payload["sub"]))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise UnauthorizedError()

        return TokenResponse(
            access_token=create_access_token(str(user.id), user.role.value),
            refresh_token=create_refresh_token(str(user.id)),
            expires_in=1800,
        )
