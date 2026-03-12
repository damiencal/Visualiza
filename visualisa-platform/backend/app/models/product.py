"""
Product Catalogue Models: Brand, Category, Product
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean, DateTime, Enum, Float, ForeignKey, Index, Integer, JSON, String, Text,
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class SurfaceType(str, PyEnum):
    FLOOR = "floor"
    WALL = "wall"
    CEILING = "ceiling"
    COUNTERTOP = "countertop"
    EXTERIOR = "exterior"
    CABINET = "cabinet"


class ProductStatus(str, PyEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
    PENDING_REVIEW = "pending_review"


class ProductSource(str, PyEnum):
    MANUAL = "manual"
    CRAWLED = "crawled"
    API = "api"


class Brand(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    country: Mapped[str] = mapped_column(String(100), default="DO")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_es: Mapped[str | None] = mapped_column(Text, nullable=True)
    crawl_base_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    products: Mapped[list["Product"]] = relationship(back_populates="brand", lazy="dynamic")


class Category(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255))
    name_es: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        CHAR(36), ForeignKey("categories.id"), nullable=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    surface_types: Mapped[list] = mapped_column(JSON, default=list)

    parent: Mapped["Category | None"] = relationship(
        "Category", remote_side="Category.id", lazy="selectin"
    )
    children: Mapped[list["Category"]] = relationship(
        "Category", back_populates="parent", lazy="selectin",
        foreign_keys="[Category.parent_id]",
    )
    products: Mapped[list["Product"]] = relationship(back_populates="category", lazy="dynamic")


class Product(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "products"
    __table_args__ = (
        Index("ix_products_brand_sku", "brand_id", "sku", unique=True),
        Index("ix_products_status_category", "status", "category_id"),
    )

    # Core fields
    name: Mapped[str] = mapped_column(String(500))
    name_es: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slug: Mapped[str] = mapped_column(String(500), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_es: Mapped[str | None] = mapped_column(Text, nullable=True)
    sku: Mapped[str] = mapped_column(String(100))

    # Pricing
    price: Mapped[float] = mapped_column(Float, nullable=False)
    original_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="DOP")
    price_unit: Mapped[str] = mapped_column(String(20), default="unit")

    # Classification
    brand_id: Mapped[uuid.UUID] = mapped_column(CHAR(36), ForeignKey("brands.id"))
    category_id: Mapped[uuid.UUID] = mapped_column(CHAR(36), ForeignKey("categories.id"))
    surface_types: Mapped[list] = mapped_column(JSON, default=list)
    tags: Mapped[list] = mapped_column(JSON, default=list)

    # Status & Source
    status: Mapped[ProductStatus] = mapped_column(
        Enum(ProductStatus), default=ProductStatus.DRAFT
    )
    source: Mapped[ProductSource] = mapped_column(
        Enum(ProductSource), default=ProductSource.MANUAL
    )
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    last_crawled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Images
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    images: Mapped[list] = mapped_column(JSON, default=list)

    # Visualizer-specific
    texture_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    texture_scale: Mapped[float] = mapped_column(Float, default=1.0)
    texture_rotation: Mapped[float] = mapped_column(Float, default=0.0)
    is_visualizer_compatible: Mapped[bool] = mapped_column(Boolean, default=False)

    # Specifications
    specifications: Mapped[dict] = mapped_column(JSON, default=dict)
    dimensions: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    colors: Mapped[list] = mapped_column(JSON, default=list)
    materials: Mapped[list] = mapped_column(JSON, default=list)

    # Stock
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    stock_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationships
    brand: Mapped["Brand"] = relationship(back_populates="products", lazy="selectin")
    category: Mapped["Category"] = relationship(back_populates="products", lazy="selectin")
    bom_line_items: Mapped[list["BomLineItem"]] = relationship(  # type: ignore[name-defined]
        back_populates="product"
    )
