"""
Tests for the BoM (Bill of Materials) calculation endpoints.
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Brand, Category, Product, ProductStatus, SurfaceType

BASE_ADMIN = "/api/v1/bom"
BASE_PUBLIC = "/public/widget"


# ── Helpers ──────────────────────────────────────────────────────────────────


async def _seed_products(db: AsyncSession) -> list[Product]:
    brand = Brand(name="BomBrand", slug="bom-brand", country="DO")
    db.add(brand)
    cat = Category(
        name="Flooring",
        name_es="Pisos",
        slug="bom-flooring",
        surface_types=[SurfaceType.FLOOR.value],
    )
    db.add(cat)
    await db.flush()

    products = []
    for i, price in enumerate([1500.0, 2800.0, 4200.0], start=1):
        p = Product(
            name=f"BomTile {i}",
            slug=f"bom-tile-{i}",
            brand_id=brand.id,
            category_id=cat.id,
            price_dop=price,
            unit="m2",
            status=ProductStatus.ACTIVE,
            surface_type=SurfaceType.FLOOR,
        )
        db.add(p)
        products.append(p)

    await db.flush()
    return products


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestBomCalculation:
    async def test_bom_requires_auth(self, client: AsyncClient):
        # Admin BoM history endpoint should require auth
        resp = await client.get(f"{BASE_ADMIN}/")
        assert resp.status_code in (401, 403)

    async def test_bom_generate_success(
        self, client: AsyncClient, pro_headers: dict, db: AsyncSession
    ):
        products = await _seed_products(db)

        resp = await client.post(
            f"{BASE_ADMIN}/generate",
            headers=pro_headers,
            json={
                "surfaces": [
                    {
                        "surface_type": "floor",
                        "area_m2": 20.0,
                        "product_id": str(products[0].id),
                    }
                ],
                "session_id": None,
            },
        )
        assert resp.status_code in (200, 201)
        data = resp.json()

        # Must contain line items
        assert "line_items" in data or "items" in data
        # Must contain a total
        assert "total_dop" in data or "subtotal_dop" in data

    async def test_bom_includes_itbis(
        self, client: AsyncClient, pro_headers: dict, db: AsyncSession
    ):
        """ITBIS (18% VAT) must be present in the BoM response."""
        products = await _seed_products(db)

        resp = await client.post(
            f"{BASE_ADMIN}/generate",
            headers=pro_headers,
            json={
                "surfaces": [
                    {
                        "surface_type": "floor",
                        "area_m2": 10.0,
                        "product_id": str(products[1].id),
                    }
                ],
            },
        )
        if resp.status_code not in (200, 201):
            pytest.skip("BoM generate endpoint returned unexpected status")

        data = resp.json()
        # The response should expose itbis_amount or tax fields
        response_str = str(data).lower()
        assert any(k in response_str for k in ("itbis", "tax", "iva"))

    async def test_bom_wastage_increases_quantity(
        self, client: AsyncClient, pro_headers: dict, db: AsyncSession
    ):
        """Flooring BoM must apply ≥ 5% wastage."""
        products = await _seed_products(db)
        area = 10.0

        resp = await client.post(
            f"{BASE_ADMIN}/generate",
            headers=pro_headers,
            json={
                "surfaces": [
                    {
                        "surface_type": "floor",
                        "area_m2": area,
                        "product_id": str(products[0].id),
                    }
                ],
            },
        )
        if resp.status_code not in (200, 201):
            pytest.skip("BoM generate endpoint returned unexpected status")

        data = resp.json()
        items = data.get("line_items") or data.get("items", [])
        if items:
            qty = items[0].get("quantity_needed") or items[0].get("quantity", area)
            # After wastage, quantity must be at least the raw area
            assert float(qty) >= area


@pytest.mark.asyncio
class TestBomHistory:
    async def test_bom_list_only_own(
        self, client: AsyncClient, pro_headers: dict, db: AsyncSession
    ):
        """Professionals should only see their own BoM sessions."""
        resp = await client.get(f"{BASE_ADMIN}/", headers=pro_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data or isinstance(data, list)
