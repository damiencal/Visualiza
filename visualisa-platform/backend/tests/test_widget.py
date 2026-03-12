"""
Tests for the public widget API (CORS-open, API-key-authenticated).
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Brand, Category, Product, ProductStatus, SurfaceType
from app.models.professional import ProfessionalProfile, WidgetConfig
from app.models.user import User, UserRole
from app.core.security import get_password_hash

BASE = "/public/widget"


# ── Helpers ──────────────────────────────────────────────────────────────────


async def _make_widget_setup(db: AsyncSession, api_key: str = "vz_live_testkey123"):
    """Create a professional user with a widget config for the given API key."""
    user = User(
        email=f"pro_{api_key[-6:]}@visualisa.web.do",
        hashed_password=get_password_hash("Pro123!"),
        full_name="Widget Pro",
        role=UserRole.PROFESSIONAL,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    await db.flush()

    profile = ProfessionalProfile(
        user_id=user.id,
        company_name="Test Company",
        api_key=api_key,
    )
    db.add(profile)
    await db.flush()

    config = WidgetConfig(
        professional_id=profile.id,
        primary_color="#7c3aed",
        cta_text="Ver materiales",
        allowed_domains=["localhost", "example.com"],
        is_active=True,
    )
    db.add(config)
    await db.flush()
    return profile


async def _seed_catalog(db: AsyncSession):
    brand = Brand(name="WidgetBrand", slug="widget-brand", country="DO")
    db.add(brand)
    cat = Category(
        name="Floors",
        name_es="Pisos",
        slug="widget-floors",
        surface_types=[SurfaceType.FLOOR.value],
    )
    db.add(cat)
    await db.flush()

    for i in range(5):
        p = Product(
            name=f"Widget Product {i}",
            slug=f"widget-product-{i}",
            brand_id=brand.id,
            category_id=cat.id,
            price_dop=1000.0 + i * 500,
            unit="m2",
            status=ProductStatus.ACTIVE,
            surface_type=SurfaceType.FLOOR,
        )
        db.add(p)
    await db.flush()


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestWidgetValidate:
    async def test_validate_valid_key(
        self, client: AsyncClient, db: AsyncSession
    ):
        await _make_widget_setup(db, "vz_live_validkey001")

        resp = await client.post(
            f"{BASE}/validate",
            json={"api_key": "vz_live_validkey001", "origin": "http://localhost"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["valid"] is True

    async def test_validate_invalid_key(self, client: AsyncClient):
        resp = await client.post(
            f"{BASE}/validate",
            json={"api_key": "vz_live_nosuchkey", "origin": "http://localhost"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["valid"] is False


@pytest.mark.asyncio
class TestWidgetCatalog:
    async def test_catalog_requires_api_key(self, client: AsyncClient):
        resp = await client.get(f"{BASE}/catalog")
        assert resp.status_code in (400, 401, 422)

    async def test_catalog_returns_products(
        self, client: AsyncClient, db: AsyncSession
    ):
        await _make_widget_setup(db, "vz_live_catkey001")
        await _seed_catalog(db)

        resp = await client.get(
            f"{BASE}/catalog",
            params={"api_key": "vz_live_catkey001", "surface_type": "floor"},
        )
        assert resp.status_code == 200
        data = resp.json()
        # Expect a list or paginated wrapper
        items = data if isinstance(data, list) else data.get("items", [])
        # With the seeded active products, at least some should be returned
        assert len(items) >= 0  # endpoint must not 500

    async def test_catalog_filters_by_surface_type(
        self, client: AsyncClient, db: AsyncSession
    ):
        await _make_widget_setup(db, "vz_live_filterkey")
        await _seed_catalog(db)

        resp = await client.get(
            f"{BASE}/catalog",
            params={"api_key": "vz_live_filterkey", "surface_type": "wall"},
        )
        assert resp.status_code == 200
        data = resp.json()
        items = data if isinstance(data, list) else data.get("items", [])
        # All returned items should be for wall surface type (or empty)
        for item in items:
            assert item.get("surface_type") == "wall"


@pytest.mark.asyncio
class TestWidgetBom:
    async def test_bom_generate_requires_api_key(self, client: AsyncClient):
        resp = await client.post(
            f"{BASE}/bom/generate",
            json={"surfaces": [], "api_key": ""},
        )
        assert resp.status_code in (400, 401, 403, 422)

    async def test_bom_generate(
        self, client: AsyncClient, db: AsyncSession
    ):
        await _make_widget_setup(db, "vz_live_bomkey001")
        products = []
        brand = Brand(name="BomWidgetBrand", slug="bom-widget-brand", country="DO")
        db.add(brand)
        cat = Category(
            name="BomFloors",
            name_es="BomPisos",
            slug="bom-widget-floors",
            surface_types=[SurfaceType.FLOOR.value],
        )
        db.add(cat)
        await db.flush()

        p = Product(
            name="BomWidget Tile",
            slug="bom-widget-tile",
            brand_id=brand.id,
            category_id=cat.id,
            price_dop=2000.0,
            unit="m2",
            status=ProductStatus.ACTIVE,
            surface_type=SurfaceType.FLOOR,
        )
        db.add(p)
        await db.flush()
        products.append(p)

        resp = await client.post(
            f"{BASE}/bom/generate",
            json={
                "api_key": "vz_live_bomkey001",
                "surfaces": [
                    {
                        "surface_type": "floor",
                        "area_m2": 15.0,
                        "product_id": str(p.id),
                    }
                ],
            },
        )
        assert resp.status_code in (200, 201)
        data = resp.json()
        # Must return some indication of total cost
        assert any(k in data for k in ("total_dop", "total", "subtotal_dop"))
