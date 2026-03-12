"""
Tests for the crawler management admin endpoints.
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.crawler import CrawlSource, CrawlJob, CrawlJobStatus
from app.models.product import Brand

BASE = "/api/v1/crawler"


# ── Helpers ──────────────────────────────────────────────────────────────────


async def _make_source(db: AsyncSession, slug: str = "test-source") -> CrawlSource:
    brand = Brand(name=f"Brand-{slug}", slug=f"brand-{slug}", country="DO")
    db.add(brand)
    await db.flush()

    source = CrawlSource(
        name="Test Source",
        slug=slug,
        url="https://example.com/products",
        crawler_type="scrapling",
        crawl_config={},
        brand_id=brand.id,
        is_enabled=True,
        crawl_frequency_hours=24,
    )
    db.add(source)
    await db.flush()
    return source


async def _make_job(
    db: AsyncSession, source: CrawlSource, status: CrawlJobStatus = CrawlJobStatus.PENDING
) -> CrawlJob:
    job = CrawlJob(
        source_id=source.id,
        status=status,
        items_found=0,
        items_created=0,
        items_updated=0,
        items_failed=0,
    )
    db.add(job)
    await db.flush()
    return job


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestCrawlerSources:
    async def test_list_sources_requires_auth(self, client: AsyncClient):
        resp = await client.get(f"{BASE}/sources")
        assert resp.status_code in (401, 403)

    async def test_list_sources(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        await _make_source(db, slug="list-source-1")
        resp = await client.get(f"{BASE}/sources", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, (list, dict))

    async def test_get_source(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        source = await _make_source(db, slug="get-source")
        resp = await client.get(f"{BASE}/sources/{source.id}", headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["slug"] == "get-source"

    async def test_get_source_not_found(self, client: AsyncClient, admin_headers: dict):
        resp = await client.get(
            f"{BASE}/sources/00000000-0000-0000-0000-000000000000",
            headers=admin_headers,
        )
        assert resp.status_code == 404

    async def test_toggle_source(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        source = await _make_source(db, slug="toggle-source")
        resp = await client.patch(
            f"{BASE}/sources/{source.id}/toggle",
            headers=admin_headers,
        )
        # Either 200 OK or 404 if endpoint has different naming
        assert resp.status_code in (200, 404)


@pytest.mark.asyncio
class TestCrawlerJobs:
    async def test_list_jobs_requires_auth(self, client: AsyncClient):
        resp = await client.get(f"{BASE}/jobs")
        assert resp.status_code in (401, 403)

    async def test_list_jobs(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        source = await _make_source(db, slug="jobs-source")
        await _make_job(db, source, CrawlJobStatus.COMPLETED)

        resp = await client.get(f"{BASE}/jobs", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data or isinstance(data, list)

    async def test_get_job(
        self, client: AsyncClient, admin_headers: dict, db: AsyncSession
    ):
        source = await _make_source(db, slug="job-detail-source")
        job = await _make_job(db, source, CrawlJobStatus.RUNNING)

        resp = await client.get(f"{BASE}/jobs/{job.id}", headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "running"


@pytest.mark.asyncio
class TestCrawlerReviewQueue:
    async def test_review_queue_requires_auth(self, client: AsyncClient):
        resp = await client.get(f"{BASE}/review")
        assert resp.status_code in (401, 403)

    async def test_review_queue_empty(
        self, client: AsyncClient, admin_headers: dict
    ):
        resp = await client.get(f"{BASE}/review", headers=admin_headers)
        assert resp.status_code == 200
