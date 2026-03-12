"""
Product schemas: Brand, Category, Product (request/response)
"""
from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl


# ── Brand ─────────────────────────────────────────────────────────────────────

class BrandBase(BaseModel):
    name: str = Field(max_length=255)
    slug: str = Field(max_length=255)
    logo_url: str | None = None
    website: str | None = None
    country: str = "DO"
    description: str | None = None
    description_es: str | None = None
    crawl_base_url: str | None = None
    is_active: bool = True


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: str | None = None
    logo_url: str | None = None
    website: str | None = None
    description: str | None = None
    description_es: str | None = None
    is_active: bool | None = None


class BrandResponse(BrandBase):
    id: str
    model_config = {"from_attributes": True}


# ── Category ──────────────────────────────────────────────────────────────────

class CategoryBase(BaseModel):
    name: str = Field(max_length=255)
    name_es: str = Field(max_length=255)
    slug: str = Field(max_length=255)
    icon: str | None = None
    parent_id: str | None = None
    sort_order: int = 0
    surface_types: list[str] = []


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    name_es: str | None = None
    icon: str | None = None
    sort_order: int | None = None
    surface_types: list[str] | None = None


class CategoryResponse(CategoryBase):
    id: str
    children: list[CategoryResponse] = []
    model_config = {"from_attributes": True}


CategoryResponse.model_rebuild()


# ── Product ───────────────────────────────────────────────────────────────────

class ProductBase(BaseModel):
    name: str = Field(max_length=500)
    name_es: str | None = None
    description: str | None = None
    description_es: str | None = None
    sku: str = Field(max_length=100)
    price: float = Field(gt=0)
    original_price: float | None = None
    currency: str = "DOP"
    price_unit: str = "unit"
    brand_id: str
    category_id: str
    surface_types: list[str] = []
    tags: list[str] = []
    thumbnail_url: str | None = None
    images: list[str] = []
    texture_url: str | None = None
    texture_scale: float = 1.0
    texture_rotation: float = 0.0
    is_visualizer_compatible: bool = False
    specifications: dict = {}
    dimensions: dict | None = None
    colors: list[str] = []
    materials: list[str] = []
    in_stock: bool = True
    stock_quantity: int | None = None


class ProductCreate(ProductBase):
    status: str = "draft"
    source: str = "manual"
    source_url: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    name_es: str | None = None
    description: str | None = None
    description_es: str | None = None
    price: float | None = None
    original_price: float | None = None
    price_unit: str | None = None
    status: str | None = None
    thumbnail_url: str | None = None
    images: list[str] | None = None
    texture_url: str | None = None
    texture_scale: float | None = None
    is_visualizer_compatible: bool | None = None
    specifications: dict | None = None
    colors: list[str] | None = None
    materials: list[str] | None = None
    tags: list[str] | None = None
    in_stock: bool | None = None
    stock_quantity: int | None = None


class ProductResponse(ProductBase):
    id: str
    slug: str
    status: str
    source: str
    source_url: str | None = None
    brand: BrandResponse | None = None
    category: CategoryResponse | None = None
    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    id: str
    name: str
    name_es: str | None = None
    slug: str
    sku: str
    price: float
    currency: str
    price_unit: str
    status: str
    thumbnail_url: str | None = None
    is_visualizer_compatible: bool
    in_stock: bool
    brand: BrandResponse | None = None
    category: CategoryResponse | None = None
    surface_types: list[str] = []
    model_config = {"from_attributes": True}
