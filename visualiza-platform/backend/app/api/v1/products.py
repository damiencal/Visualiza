"""
Products API router (Admin)
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.models.user import User
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationParams
from app.schemas.product import (
    BrandCreate, BrandResponse, BrandUpdate,
    CategoryCreate, CategoryResponse, CategoryUpdate,
    ProductCreate, ProductListResponse, ProductResponse, ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products (Admin)"])


@router.get("/", response_model=PaginatedResponse[ProductListResponse])
async def list_products(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    status: str | None = None,
    brand_id: str | None = None,
    category_id: str | None = None,
    search: str | None = None,
    source: str | None = None,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    pagination = PaginationParams(page=page, limit=limit)
    products, total = await ProductService.list_products(
        db, pagination, status, brand_id, category_id, None, search, source
    )
    pages = (total + limit - 1) // limit
    return PaginatedResponse(items=products, total=total, page=page, limit=limit, pages=pages)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return await ProductService.create_product(data, db)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return await ProductService.get_product(product_id, db)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return await ProductService.update_product(product_id, data, db)


@router.delete("/{product_id}", response_model=MessageResponse)
async def delete_product(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    await ProductService.delete_product(product_id, db)
    return MessageResponse(message="Producto desactivado")


@router.post("/bulk-approve", response_model=MessageResponse)
async def bulk_approve(
    product_ids: list[str],
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    count = await ProductService.bulk_approve(product_ids, db)
    return MessageResponse(message=f"{count} productos aprobados")


@router.post("/bulk-status", response_model=MessageResponse)
async def bulk_status(
    product_ids: list[str],
    status: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    count = await ProductService.bulk_status(product_ids, status, db)
    return MessageResponse(message=f"{count} productos actualizados")


# ── Brands ─────────────────────────────────────────────────────────────────

brands_router = APIRouter(prefix="/brands", tags=["Brands (Admin)"])


@brands_router.get("/", response_model=list[BrandResponse])
async def list_brands(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return await ProductService.list_brands(db)


@brands_router.post("/", response_model=BrandResponse, status_code=201)
async def create_brand(
    data: BrandCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    from app.models.product import Brand
    brand = Brand(**data.model_dump())
    db.add(brand)
    await db.flush()
    return brand


@brands_router.put("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: str,
    data: BrandUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    brand = await ProductService.get_brand(brand_id, db)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(brand, key, value)
    await db.flush()
    return brand


# ── Categories ─────────────────────────────────────────────────────────────

categories_router = APIRouter(prefix="/categories", tags=["Categories (Admin)"])


@categories_router.get("/", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await ProductService.list_categories(db)


@categories_router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    from app.models.product import Category
    category = Category(**data.model_dump())
    db.add(category)
    await db.flush()
    return category
