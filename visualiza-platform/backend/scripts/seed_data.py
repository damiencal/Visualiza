#!/usr/bin/env python3
"""
Seed the Visualiza database with initial reference data.

Usage:
    cd visualiza-platform/backend
    python scripts/seed_data.py

Requires the following env vars (or a .env file in the backend directory):
    DATABASE_URL, SYNC_DATABASE_URL, SECRET_KEY
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

# Make sure the app package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv  # type: ignore

load_dotenv(Path(__file__).parent.parent / ".env")

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, engine
from app.models.base import Base
from app.models.billing import Plan, PlanTier
from app.models.crawler import CrawlSource
from app.models.product import Brand, Category, SurfaceType
from app.models.user import User, UserRole
from app.core.security import get_password_hash

# ── Helpers ──────────────────────────────────────────────────────────────────


async def _exists(session: AsyncSession, model, **kwargs) -> bool:
    result = await session.execute(select(model).filter_by(**kwargs))
    return result.scalars().first() is not None


# ── Seed functions ────────────────────────────────────────────────────────────


async def seed_brands(session: AsyncSession) -> dict[str, Brand]:
    brands_data = [
        {
            "name": "Aliss",
            "slug": "aliss",
            "website": "https://www.aliss.com.do",
            "country": "DO",
            "description": "Leading home appliance and construction materials retailer in the DR.",
            "description_es": "Principal minorista de electrodomésticos y materiales de construcción en RD.",
            "crawl_base_url": "https://www.aliss.com.do",
            "is_active": True,
        },
        {
            "name": "Ochoa",
            "slug": "ochoa",
            "website": "https://www.ochoa.com.do",
            "country": "DO",
            "description": "Dominican hardware and home improvement mega-store.",
            "description_es": "Mega ferretería dominicana para el mejoramiento del hogar.",
            "crawl_base_url": "https://www.ochoa.com.do",
            "is_active": True,
        },
        {
            "name": "Mister C",
            "slug": "mister-c",
            "website": "https://www.misterc.com.do",
            "country": "DO",
            "description": "Electronics and home products retailer.",
            "description_es": "Distribuidora de electrónicos y artículos para el hogar.",
            "crawl_base_url": "https://www.misterc.com.do",
            "is_active": True,
        },
        {
            "name": "Cemex",
            "slug": "cemex",
            "website": "https://www.cemex.com.do",
            "country": "DO",
            "description": "Cement and construction materials leader.",
            "description_es": "Líder en cemento y materiales de construcción.",
            "is_active": True,
        },
        {
            "name": "FERSAN",
            "slug": "fersan",
            "website": "https://fersan.com.do",
            "country": "DO",
            "description": "Hardware, plumbing and electrical supplies.",
            "description_es": "Ferretería, plomería y materiales eléctricos.",
            "is_active": True,
        },
        {
            "name": "Porcelanite",
            "slug": "porcelanite",
            "website": "https://www.porcelanite.com",
            "country": "MX",
            "description": "Premium ceramic and porcelain tile brand.",
            "description_es": "Marca líder de pisos cerámicos y porcelanatos.",
            "is_active": True,
        },
        {
            "name": "Keraben",
            "slug": "keraben",
            "website": "https://www.keraben.com",
            "country": "ES",
            "description": "Spanish porcelain tile manufacturer.",
            "description_es": "Fabricante español de porcelanato.",
            "is_active": True,
        },
        {
            "name": "Sherwin Williams",
            "slug": "sherwin-williams",
            "website": "https://www.sherwin-williams.com",
            "country": "US",
            "description": "Global paint and coatings leader.",
            "description_es": "Empresa líder mundial en pinturas y recubrimientos.",
            "is_active": True,
        },
        {
            "name": "InterAmerica",
            "slug": "interamerica",
            "website": "https://www.interamerica.com.do",
            "country": "DO",
            "description": "Dominican furniture and interior design stores.",
            "description_es": "Tiendas de muebles y diseño interior dominicanas.",
            "is_active": True,
        },
        {
            "name": "Ikea DR",
            "slug": "ikea-dr",
            "website": "https://www.ikea.com/us/en/",
            "country": "SE",
            "description": "Affordable flat-pack furniture and home accessories.",
            "description_es": "Muebles asequibles y accesorios para el hogar.",
            "is_active": True,
        },
    ]

    result: dict[str, Brand] = {}
    for data in brands_data:
        if not await _exists(session, Brand, slug=data["slug"]):
            brand = Brand(**data)
            session.add(brand)
            result[data["slug"]] = brand
            print(f"  + brand: {data['name']}")
        else:
            r = await session.execute(select(Brand).filter_by(slug=data["slug"]))
            result[data["slug"]] = r.scalars().first()

    await session.flush()
    return result


async def seed_categories(session: AsyncSession) -> dict[str, Category]:
    categories_data = [
        {
            "name": "Flooring",
            "name_es": "Pisos",
            "slug": "flooring",
            "icon": "ph:squares-four",
            "surface_types": [SurfaceType.FLOOR],
            "sort_order": 1,
        },
        {
            "name": "Wall Tiles",
            "name_es": "Azulejos de Pared",
            "slug": "wall-tiles",
            "icon": "ph:wall",
            "surface_types": [SurfaceType.WALL],
            "sort_order": 2,
        },
        {
            "name": "Paint",
            "name_es": "Pinturas",
            "slug": "paint",
            "icon": "ph:paint-bucket",
            "surface_types": [SurfaceType.WALL, SurfaceType.CEILING, SurfaceType.EXTERIOR],
            "sort_order": 3,
        },
        {
            "name": "Countertops",
            "name_es": "Encimeras",
            "slug": "countertops",
            "icon": "ph:table",
            "surface_types": [SurfaceType.COUNTERTOP],
            "sort_order": 4,
        },
        {
            "name": "Ceiling Materials",
            "name_es": "Materiales de Techo",
            "slug": "ceiling",
            "icon": "ph:house-line",
            "surface_types": [SurfaceType.CEILING],
            "sort_order": 5,
        },
        {
            "name": "Exterior Cladding",
            "name_es": "Revestimiento Exterior",
            "slug": "exterior",
            "icon": "ph:buildings",
            "surface_types": [SurfaceType.EXTERIOR],
            "sort_order": 6,
        },
        {
            "name": "Cabinet & Millwork",
            "name_es": "Gabinetes y Carpintería",
            "slug": "cabinets",
            "icon": "ph:dresser",
            "surface_types": [SurfaceType.CABINET],
            "sort_order": 7,
        },
        {
            "name": "Stone & Marble",
            "name_es": "Piedra y Mármol",
            "slug": "stone-marble",
            "icon": "ph:diamond",
            "surface_types": [SurfaceType.FLOOR, SurfaceType.WALL, SurfaceType.COUNTERTOP],
            "sort_order": 8,
        },
        {
            "name": "Vinyl & Laminate",
            "name_es": "Vinilo y Laminado",
            "slug": "vinyl-laminate",
            "icon": "ph:layout",
            "surface_types": [SurfaceType.FLOOR],
            "sort_order": 9,
        },
        {
            "name": "Adhesives & Grout",
            "name_es": "Adhesivos y Fragüe",
            "slug": "adhesives-grout",
            "icon": "ph:drop",
            "surface_types": [SurfaceType.FLOOR, SurfaceType.WALL],
            "sort_order": 10,
        },
    ]

    result: dict[str, Category] = {}
    for data in categories_data:
        if not await _exists(session, Category, slug=data["slug"]):
            cat = Category(**{**data, "surface_types": [s.value for s in data["surface_types"]]})
            session.add(cat)
            result[data["slug"]] = cat
            print(f"  + category: {data['name_es']}")
        else:
            r = await session.execute(select(Category).filter_by(slug=data["slug"]))
            result[data["slug"]] = r.scalars().first()

    await session.flush()
    return result


async def seed_plans(session: AsyncSession) -> list[Plan]:
    plans_data = [
        {
            "name": "Starter",
            "name_es": "Iniciador",
            "tier": PlanTier.STARTER,
            "description": "Perfect for individual professionals getting started.",
            "description_es": "Ideal para profesionales individuales que comienzan.",
            "price_monthly_usd": 29.0,
            "price_yearly_usd": 290.0,
            "max_visualizations_per_month": 100,
            "max_bom_exports_per_month": 50,
            "max_domains": 1,
            "max_api_calls_per_day": 500,
            "includes_analytics": False,
            "includes_custom_branding": False,
            "includes_priority_support": False,
            "features": [
                "100 visualizaciones/mes",
                "50 exportaciones BoM/mes",
                "1 dominio",
                "Widget embedible",
                "Soporte por email",
            ],
            "sort_order": 1,
        },
        {
            "name": "Professional",
            "name_es": "Profesional",
            "tier": PlanTier.PROFESSIONAL,
            "description": "For growing design firms and real estate agencies.",
            "description_es": "Para firmas de diseño y agencias inmobiliarias en crecimiento.",
            "price_monthly_usd": 99.0,
            "price_yearly_usd": 990.0,
            "max_visualizations_per_month": 500,
            "max_bom_exports_per_month": 200,
            "max_domains": 5,
            "max_api_calls_per_day": 5000,
            "includes_analytics": True,
            "includes_custom_branding": True,
            "includes_priority_support": False,
            "features": [
                "500 visualizaciones/mes",
                "200 exportaciones BoM/mes",
                "5 dominios",
                "Analytics avanzados",
                "Branding personalizado",
                "Widget embedible",
                "Soporte prioritario",
            ],
            "sort_order": 2,
        },
        {
            "name": "Enterprise",
            "name_es": "Empresarial",
            "tier": PlanTier.ENTERPRISE,
            "description": "Unlimited usage for large enterprises and platforms.",
            "description_es": "Uso ilimitado para grandes empresas y plataformas.",
            "price_monthly_usd": 299.0,
            "price_yearly_usd": 2990.0,
            "max_visualizations_per_month": -1,  # -1 == unlimited
            "max_bom_exports_per_month": -1,
            "max_domains": -1,
            "max_api_calls_per_day": -1,
            "includes_analytics": True,
            "includes_custom_branding": True,
            "includes_priority_support": True,
            "features": [
                "Visualizaciones ilimitadas",
                "Exportaciones BoM ilimitadas",
                "Dominios ilimitados",
                "Analytics avanzados",
                "Branding personalizado",
                "API dedicada",
                "Soporte SLA 99.9%",
                "Gerente de cuenta dedicado",
            ],
            "sort_order": 3,
        },
    ]

    created: list[Plan] = []
    for data in plans_data:
        if not await _exists(session, Plan, tier=data["tier"]):
            plan = Plan(**data)
            session.add(plan)
            created.append(plan)
            print(f"  + plan: {data['name_es']}")

    await session.flush()
    return created


async def seed_crawl_sources(session: AsyncSession, brands: dict[str, Brand]) -> None:
    sources_data = [
        {
            "name": "Aliss — Pisos y Azulejos",
            "slug": "aliss-tiles",
            "brand_slug": "aliss",
            "url": "https://www.aliss.com.do/categoria/pisos-y-azulejos",
            "crawler_type": "scrapling",
            "crawl_config": {
                "selectors": {
                    "product_list": ".product-item",
                    "name": ".product-title",
                    "price": ".product-price",
                    "image": "img.product-image",
                    "url": "a.product-link",
                },
                "pagination": {"next_page_selector": ".pagination .next", "max_pages": 20},
                "surface_type_hint": "floor",
            },
            "is_enabled": True,
            "crawl_frequency_hours": 24,
        },
        {
            "name": "Ochoa — Pinturas",
            "slug": "ochoa-paint",
            "brand_slug": "ochoa",
            "url": "https://www.ochoa.com.do/pinturas",
            "crawler_type": "scrapling",
            "crawl_config": {
                "selectors": {
                    "product_list": ".listing-item",
                    "name": "h3.name",
                    "price": "span.price",
                    "image": "img",
                    "url": "a",
                },
                "pagination": {"next_page_selector": "a.next", "max_pages": 15},
                "surface_type_hint": "wall",
            },
            "is_enabled": True,
            "crawl_frequency_hours": 24,
        },
        {
            "name": "Mister C — Encimeras y Muebles",
            "slug": "misterc-countertops",
            "brand_slug": "mister-c",
            "url": "https://www.misterc.com.do/cocina/encimeras",
            "crawler_type": "scrapling",
            "crawl_config": {
                "selectors": {
                    "product_list": ".prod-card",
                    "name": ".prod-name",
                    "price": ".prod-price",
                    "image": "img.main",
                    "url": "a.prod-link",
                },
                "pagination": {"next_page_selector": ".page-next", "max_pages": 10},
                "surface_type_hint": "countertop",
            },
            "is_enabled": True,
            "crawl_frequency_hours": 48,
        },
    ]

    for data in sources_data:
        brand_slug = data.pop("brand_slug")
        brand = brands.get(brand_slug)
        if brand and not await _exists(session, CrawlSource, slug=data["slug"]):
            source = CrawlSource(**data, brand_id=brand.id)
            session.add(source)
            print(f"  + crawl source: {data['name']}")

    await session.flush()


async def seed_admin_user(session: AsyncSession) -> None:
    email = os.getenv("SEED_ADMIN_EMAIL", "admin@visualiza.do")
    password = os.getenv("SEED_ADMIN_PASSWORD", "Admin1234!")

    if not await _exists(session, User, email=email):
        admin = User(
            email=email,
            hashed_password=get_password_hash(password),
            full_name="Visualiza Admin",
            role=UserRole.SUPERADMIN,
            is_active=True,
            is_verified=True,
        )
        session.add(admin)
        print(f"  + superadmin: {email}")
    else:
        print(f"  ~ superadmin already exists: {email}")


# ── Main ──────────────────────────────────────────────────────────────────────


async def main() -> None:
    print("=== Visualiza Seed Data ===")
    async with AsyncSessionLocal() as session:
        async with session.begin():
            print("\n[Brands]")
            brands = await seed_brands(session)

            print("\n[Categories]")
            await seed_categories(session)

            print("\n[Plans]")
            await seed_plans(session)

            print("\n[Crawl Sources]")
            await seed_crawl_sources(session, brands)

            print("\n[Admin User]")
            await seed_admin_user(session)

    print("\n✅ Seed complete.")


if __name__ == "__main__":
    asyncio.run(main())
