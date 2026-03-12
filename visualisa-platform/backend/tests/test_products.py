"""
Tests for the product catalog admin endpoints.
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Brand, Category, Product, ProductStatus, SurfaceType

BASE = "/api/v1/products"


# ── Helpers ──────────────────────────────────────────────────────────────────


async def _make_brand(db: AsyncSession, name: str = "TestBrand") -> Brand:
    brand = Brand(name=name, slug=name.lower().replace(" ", "-"), country="DO")
    db.add(brand)
    await db.flush()
    return brand


async def _make_category(db: AsyncSession, name: str = "Flooring") -> Category:
    cat = Category(
        name=name,
        name_es=name,
        slug=name.lower().replace(" ", "-"),
        surface_types=[SurfaceType.FLOOR.value],
    )
    db.add(cat)
    await db.flush()
    return cat


async def _make_product(
    db: AsyncSession,
    *,
    brand: Brand,
    category: Category,
    name: str = "Test Tile",
) -> Product:
    product = Product(
        name=name,
        slug=name.lower().replace(" ", "-"),
        brand_id=brand.id,
        category_id=category.id,
        price_dop=1500.0,
        unit="m2",
        status=ProductStatus.ACTIVE,
        surface_type=SurfaceType.FLOOR,
    )
    db.add(product)
    await db.flush()
    return product


# ── Tests ────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestProductList:
    async def test_list_requires_auth(self, client: AsyncClient):
        resp = await client.get(BASE + "/")
        assert resp.status_code in (401, 403)

    async def test_list_returns_paginated(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        brand = await _make_brand(db)
        category = await _make_category(db)
        await _make_product(db, brand=brand, category=category, name="Porcelain A")
        await _make_product(db, brand=brand, category=category, name="Porcelain B")

        resp = await client.get(BASE + "/", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 2

    async def test_list_search_filter(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        brand = await _make_brand(db, "SearchBrand")
        category = await _make_category(db, "SearchCat")
        await _make_product(db, brand=brand, category=category, name="Unique Search Term XYZ")

        resp = await client.get(BASE + "/?search=XYZ", headers=admin_headers)
        assert resp.status_code == 200
        items = resp.json()["items"]
        assert any("XYZ" in p["name"] for p in items)


@pytest.mark.asyncio
class TestProductCreate:
    async def test_create_product(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        brand = await _make_brand(db, "CreateBrand")
        category = await _make_category(db, "CreateCat")

        resp = await client.post(
            BASE + "/",
            headers=admin_headers,
            json={
                "name": "New Tile",
                "brand_id": str(brand.id),
                "category_id": str(category.id),
                "price_dop": 2500.0,
                "unit": "m2",
                "surface_type": "floor",
                "status": "active",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "New Tile"
        assert "id" in data

    async def test_create_requires_admin(self, client: AsyncClient, pro_headers: dict):
        resp = await client.post(
            BASE + "/",
            headers=pro_headers,
            json={"name": "X", "price_dop": 100, "unit": "m2", "surface_type": "floor"},
        )
        assert resp.status_code in (401, 403)


@pytest.mark.asyncio
class TestProductDetail:
    async def test_get_product(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        brand = await _make_brand(db, "DetailBrand")
        category = await _make_category(db, "DetailCat")
        product = await _make_product(db, brand=brand, category=category, name="Detail Tile")

        resp = await client.get(f"{BASE}/{product.id}", headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Detail Tile"

    async def test_get_product_not_found(self, client: AsyncClient, admin_headers: dict):
        resp = await client.get(
            f"{BASE}/00000000-0000-0000-0000-000000000000", headers=admin_headers
        )
        assert resp.status_code == 404


@pytest.mark.asyncio
class TestProductUpdate:
    async def test_update_product(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        brand = await _make_brand(db, "UpdateBrand")
        category = await _make_category(db, "UpdateCat")
        product = await _make_product(db, brand=brand, category=category, name="Old Name")

        resp = await client.put(
            f"{BASE}/{product.id}",
            headers=admin_headers,
            json={"name": "New Name", "price_dop": 3000.0},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "New Name"

    async def test_delete_product(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        brand = await _make_brand(db, "DelBrand")
        category = await _make_category(db, "DelCat")
        product = await _make_product(db, brand=brand, category=category, name="To Delete")

        resp = await client.delete(f"{BASE}/{product.id}", headers=admin_headers)
        assert resp.status_code in (200, 204)
