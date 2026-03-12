"""
Product service: CRUD, bulk approve, status management
"""
import math
from typing import Any

from slugify import slugify
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.product import Brand, Category, Product, ProductSource, ProductStatus
from app.schemas.common import PaginationParams
from app.schemas.product import ProductCreate, ProductListResponse, ProductUpdate


class ProductService:
    @staticmethod
    async def list_products(
        db: AsyncSession,
        pagination: PaginationParams,
        status: str | None = None,
        brand_id: str | None = None,
        category_id: str | None = None,
        surface_type: str | None = None,
        search: str | None = None,
        source: str | None = None,
    ) -> tuple[list[Product], int]:
        q = select(Product)
        if status:
            q = q.where(Product.status == status)
        if brand_id:
            q = q.where(Product.brand_id == brand_id)
        if category_id:
            q = q.where(Product.category_id == category_id)
        if source:
            q = q.where(Product.source == source)
        if search:
            q = q.where(Product.name.ilike(f"%{search}%"))

        count_q = select(func.count()).select_from(q.subquery())
        total = (await db.execute(count_q)).scalar_one()

        q = q.offset(pagination.offset).limit(pagination.limit)
        result = await db.execute(q)
        return result.scalars().all(), total

    @staticmethod
    async def get_product(product_id: str, db: AsyncSession) -> Product:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise NotFoundError("Producto")
        return product

    @staticmethod
    async def create_product(data: ProductCreate, db: AsyncSession) -> Product:
        slug = slugify(data.name)
        # Ensure slug uniqueness
        existing = await db.execute(select(Product).where(Product.slug == slug))
        if existing.scalar_one_or_none():
            slug = f"{slug}-{data.sku}"

        product = Product(
            **data.model_dump(exclude={"status", "source", "source_url"}),
            slug=slug,
            status=ProductStatus(data.status),
            source=ProductSource(data.source),
            source_url=data.source_url,
        )
        db.add(product)
        await db.flush()
        return product

    @staticmethod
    async def update_product(
        product_id: str, data: ProductUpdate, db: AsyncSession
    ) -> Product:
        product = await ProductService.get_product(product_id, db)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        await db.flush()
        return product

    @staticmethod
    async def delete_product(product_id: str, db: AsyncSession) -> None:
        product = await ProductService.get_product(product_id, db)
        product.status = ProductStatus.INACTIVE
        await db.flush()

    @staticmethod
    async def bulk_approve(product_ids: list[str], db: AsyncSession) -> int:
        """Approve crawled products (set status to ACTIVE)."""
        count = 0
        for pid in product_ids:
            result = await db.execute(select(Product).where(Product.id == pid))
            product = result.scalar_one_or_none()
            if product:
                product.status = ProductStatus.ACTIVE
                count += 1
        await db.flush()
        return count

    @staticmethod
    async def bulk_status(
        product_ids: list[str], status: str, db: AsyncSession
    ) -> int:
        count = 0
        for pid in product_ids:
            result = await db.execute(select(Product).where(Product.id == pid))
            product = result.scalar_one_or_none()
            if product:
                product.status = ProductStatus(status)
                count += 1
        await db.flush()
        return count

    # ── Brands ────────────────────────────────────────────────────────────────

    @staticmethod
    async def list_brands(db: AsyncSession) -> list[Brand]:
        result = await db.execute(select(Brand).order_by(Brand.name))
        return result.scalars().all()

    @staticmethod
    async def get_brand(brand_id: str, db: AsyncSession) -> Brand:
        result = await db.execute(select(Brand).where(Brand.id == brand_id))
        brand = result.scalar_one_or_none()
        if not brand:
            raise NotFoundError("Marca")
        return brand

    # ── Categories ────────────────────────────────────────────────────────────

    @staticmethod
    async def list_categories(db: AsyncSession) -> list[Category]:
        result = await db.execute(
            select(Category).where(Category.parent_id.is_(None)).order_by(Category.sort_order)
        )
        return result.scalars().all()
