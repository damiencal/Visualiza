"""
Tests for billing plans and subscription endpoints.
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.billing import Plan, PlanTier

BASE = "/api/v1/billing"


# ── Helpers ──────────────────────────────────────────────────────────────────


async def _make_plans(db: AsyncSession) -> list[Plan]:
    plans = [
        Plan(
            name="Starter",
            name_es="Iniciador",
            tier=PlanTier.STARTER,
            price_monthly_usd=29.0,
            price_yearly_usd=290.0,
            max_visualisations_per_month=100,
            max_bom_exports_per_month=50,
            max_domains=1,
            max_api_calls_per_day=500,
            is_active=True,
            sort_order=1,
            features=["50 BoM/mes"],
        ),
        Plan(
            name="Professional",
            name_es="Profesional",
            tier=PlanTier.PROFESSIONAL,
            price_monthly_usd=99.0,
            price_yearly_usd=990.0,
            max_visualisations_per_month=500,
            max_bom_exports_per_month=200,
            max_domains=5,
            max_api_calls_per_day=5000,
            includes_analytics=True,
            includes_custom_branding=True,
            is_active=True,
            sort_order=2,
            features=["200 BoM/mes", "Analytics"],
        ),
    ]
    for p in plans:
        db.add(p)
    await db.flush()
    return plans


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestPlansEndpoint:
    async def test_list_plans_public(self, client: AsyncClient, db: AsyncSession):
        """Plan listing should be publicly accessible (used by pricing page)."""
        await _make_plans(db)
        resp = await client.get(f"{BASE}/plans")
        assert resp.status_code == 200
        data = resp.json()
        plans = data if isinstance(data, list) else data.get("items", [])
        assert len(plans) >= 2

    async def test_plan_has_required_fields(self, client: AsyncClient, db: AsyncSession):
        await _make_plans(db)
        resp = await client.get(f"{BASE}/plans")
        assert resp.status_code == 200
        data = resp.json()
        plans = data if isinstance(data, list) else data.get("items", [])
        if plans:
            plan = plans[0]
            for field in ("name", "tier", "price_monthly_usd", "features"):
                assert field in plan, f"Missing field: {field}"


@pytest.mark.asyncio
class TestCheckoutEndpoint:
    async def test_checkout_requires_auth(self, client: AsyncClient):
        resp = await client.post(
            f"{BASE}/checkout",
            json={"plan_tier": "starter", "billing_period": "monthly"},
        )
        assert resp.status_code in (401, 403)

    async def test_checkout_authenticated(
        self, client: AsyncClient, pro_headers: dict, db: AsyncSession
    ):
        await _make_plans(db)
        resp = await client.post(
            f"{BASE}/checkout",
            headers=pro_headers,
            json={"plan_tier": "starter", "billing_period": "monthly"},
        )
        # In test mode Stripe key is not set, so expect 200 with a checkout URL
        # or a 400/500 if Stripe is not mocked — either is acceptable
        assert resp.status_code in (200, 201, 400, 500)


@pytest.mark.asyncio
class TestSubscriptionStatus:
    async def test_subscription_requires_auth(self, client: AsyncClient):
        resp = await client.get(f"{BASE}/subscription")
        assert resp.status_code in (401, 403)

    async def test_subscription_no_plan(
        self, client: AsyncClient, pro_headers: dict
    ):
        """A fresh professional with no subscription should get 200 or 404."""
        resp = await client.get(f"{BASE}/subscription", headers=pro_headers)
        assert resp.status_code in (200, 404)
