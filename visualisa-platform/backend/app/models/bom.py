"""
Bill of Materials Models
"""
import uuid

from sqlalchemy import Float, ForeignKey, JSON, String, Text, Boolean
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class BillOfMaterials(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "bills_of_materials"

    professional_id: Mapped[uuid.UUID | None] = mapped_column(
        CHAR(36), ForeignKey("professional_profiles.id"), nullable=True
    )
    session_id: Mapped[uuid.UUID | None] = mapped_column(CHAR(36), nullable=True)

    # Room details
    room_type: Mapped[str] = mapped_column(String(50))
    room_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rendered_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Surface measurements from AI segmentation or manual input
    measurements: Mapped[dict] = mapped_column(JSON, default=dict)

    # Totals (DOP)
    subtotal: Mapped[float] = mapped_column(Float, default=0.0)
    tax_rate: Mapped[float] = mapped_column(Float, default=0.18)  # DR ITBIS 18%
    tax_amount: Mapped[float] = mapped_column(Float, default=0.0)
    total: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), default="DOP")

    # Sharing
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_shared: Mapped[bool] = mapped_column(Boolean, default=False)
    share_token: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True)

    # Relationships
    line_items: Mapped[list["BomLineItem"]] = relationship(
        back_populates="bom", cascade="all, delete-orphan", lazy="selectin"
    )
    professional: Mapped["ProfessionalProfile | None"] = relationship(  # type: ignore[name-defined]
        back_populates="bills_of_materials", lazy="selectin"
    )


class BomLineItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "bom_line_items"

    bom_id: Mapped[uuid.UUID] = mapped_column(
        CHAR(36), ForeignKey("bills_of_materials.id")
    )
    product_id: Mapped[uuid.UUID] = mapped_column(CHAR(36), ForeignKey("products.id"))

    surface_type: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(20))
    unit_price: Mapped[float] = mapped_column(Float)
    line_total: Mapped[float] = mapped_column(Float)

    # Wastage factor: 10–15% for flooring/tile, 5% for paint
    wastage_percent: Mapped[float] = mapped_column(Float, default=10.0)
    quantity_with_wastage: Mapped[float] = mapped_column(Float)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    bom: Mapped["BillOfMaterials"] = relationship(back_populates="line_items")
    product: Mapped["Product"] = relationship(  # type: ignore[name-defined]
        back_populates="bom_line_items", lazy="selectin"
    )
