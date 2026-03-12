"""
ProfessionalProfile, WidgetDeployment Models
"""
import uuid
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Enum, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class ProfessionalType(str, PyEnum):
    AGENT = "agent"
    BROKERAGE = "brokerage"
    MLS = "mls"
    DEVELOPER = "developer"
    PROPERTY_MANAGER = "property_manager"


class ProfessionalProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "professional_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        CHAR(36), ForeignKey("users.id"), unique=True
    )
    professional_type: Mapped[ProfessionalType] = mapped_column(Enum(ProfessionalType))
    company_name: Mapped[str] = mapped_column(String(255))
    company_website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    license_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100))
    province: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100), default="DO")
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Widget configuration stored as JSON
    widget_config: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # API key for widget authentication (public key, hashed secret)
    api_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    api_key_secret_hash: Mapped[str] = mapped_column(String(255))

    # Relationships
    user: Mapped["User"] = relationship(back_populates="professional_profile")  # type: ignore[name-defined]
    widget_deployments: Mapped[list["WidgetDeployment"]] = relationship(
        back_populates="professional", cascade="all, delete-orphan"
    )
    bills_of_materials: Mapped[list["BillOfMaterials"]] = relationship(  # type: ignore[name-defined]
        back_populates="professional", lazy="dynamic"
    )


class WidgetDeployment(Base, UUIDMixin, TimestampMixin):
    """Tracks authorized domains for widget deployment."""
    __tablename__ = "widget_deployments"

    professional_id: Mapped[uuid.UUID] = mapped_column(
        CHAR(36), ForeignKey("professional_profiles.id")
    )
    domain: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    allowed_origins: Mapped[list] = mapped_column(JSON, default=list)
    custom_css: Mapped[str | None] = mapped_column(Text, nullable=True)
    button_text: Mapped[str] = mapped_column(String(50), default="Redecorar")
    button_position: Mapped[str] = mapped_column(String(20), default="bottom-right")

    professional: Mapped["ProfessionalProfile"] = relationship(
        back_populates="widget_deployments"
    )
