"""
Auth router
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest, LoginRequest, RefreshRequest,
    RegisterRequest, ResetPasswordRequest, TokenResponse, UserResponse,
)
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)) -> User:
    user = await AuthService.register(data, db)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await AuthService.login(data.email, data.password, db)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await AuthService.refresh(data.refresh_token, db)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)
) -> MessageResponse:
    # In production: send reset email via email service
    return MessageResponse(
        message="Si el correo existe, recibirás un enlace de restablecimiento"
    )


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)
) -> MessageResponse:
    from app.core.security import hash_password, verify_password_reset_token
    from sqlalchemy import select
    from app.models.user import User as UserModel

    email = verify_password_reset_token(data.token)
    if not email:
        from app.core.exceptions import UnauthorizedError
        raise UnauthorizedError("Token de restablecimiento inválido o expirado")

    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if user:
        user.hashed_password = hash_password(data.new_password)
    return MessageResponse(message="Contraseña restablecida exitosamente")
