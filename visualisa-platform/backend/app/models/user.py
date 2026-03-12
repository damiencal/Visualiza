"""
User, Role, Auth Models
"""
import uuid
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class UserRole(str, PyEnum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    PROFESSIONAL = "professional"


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.PROFESSIONAL)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Relationships
    professional_profile: Mapped["ProfessionalProfile"] = relationship(  # type: ignore[name-defined]
        back_populates="user", uselist=False, lazy="selectin"
    )
    subscriptions: Mapped[list["Subscription"]] = relationship(  # type: ignore[name-defined]
        back_populates="user", lazy="selectin"
    )
