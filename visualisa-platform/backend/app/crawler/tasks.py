"""
Celery tasks for crawl execution
"""
from __future__ import annotations

from datetime import datetime, timezone

from celery import shared_task
from sqlalchemy import select

from app.database import get_sync_session
from app.models.crawler import CrawlJob, CrawlResult, CrawlSource, CrawlStatus
from app.crawler.aliss import AlissCrawler
from app.crawler.ochoa import OchoaCrawler
from app.crawler.ikea_dr import IkeaDRCrawler
from app.crawler.pipeline import ProductPipeline

CRAWLER_REGISTRY: dict[str, type] = {
    "AlissCrawler": AlissCrawler,
    "OchoaCrawler": OchoaCrawler,
    "IkeaDRCrawler": IkeaDRCrawler,
}


@shared_task(bind=True, max_retries=2, default_retry_delay=300, name="crawler.execute_crawl_job")
def execute_crawl_job(self, job_id: str) -> dict:  # type: ignore[override]
    """Execute a crawl job by ID."""
    pipeline = ProductPipeline()

    with get_sync_session() as session:
        job = session.get(CrawlJob, job_id)
        if not job:
            return {"error": "Job not found"}

        source: CrawlSource = job.source
        crawler_cls = CRAWLER_REGISTRY.get(source.crawler_class)
        if not crawler_cls:
            job.status = CrawlStatus.FAILED
            job.errors = [{"message": f"Unknown crawler: {source.crawler_class}"}]
            session.commit()
            return {"error": f"Unknown crawler: {source.crawler_class}"}

        job.status = CrawlStatus.RUNNING
        job.started_at = datetime.now(timezone.utc)
        session.commit()

        try:
            crawler = crawler_cls(config=source.config)
            products = crawler.crawl()

            for product in products:
                normalized = pipeline.process(product, source.name)

                # Dedup check
                existing = session.execute(
                    select(CrawlResult).where(
                        CrawlResult.dedup_hash == normalized.get("dedup_hash")
                    )
                ).scalar_one_or_none()

                result = CrawlResult(
                    job_id=job.id,
                    raw_data=normalized["raw_data"],
                    source_url=product.source_url,
                    source_sku=product.source_sku,
                    normalized_name=normalized["normalized_name"],
                    normalized_price=normalized["normalized_price"],
                    normalized_currency=normalized["normalized_currency"],
                    normalized_category=normalized["normalized_category"],
                    normalized_images=normalized["normalized_images"],
                    dedup_hash=normalized["dedup_hash"],
                    is_duplicate=existing is not None,
                )
                session.add(result)
                job.products_found += 1

            job.status = CrawlStatus.COMPLETED
            job.completed_at = datetime.now(timezone.utc)
            job.duration_seconds = (job.completed_at - job.started_at).total_seconds()
            session.commit()
            return {"products_found": job.products_found}

        except Exception as e:
            job.status = CrawlStatus.FAILED
            job.errors = [{"message": str(e)}]
            job.completed_at = datetime.now(timezone.utc)
            session.commit()
            raise self.retry(exc=e)


@shared_task(name="crawler.scheduled_crawl")
def scheduled_crawl(source_slug: str) -> dict:
    """Triggered by Celery Beat scheduler."""
    with get_sync_session() as session:
        source = session.execute(
            select(CrawlSource).where(CrawlSource.slug == source_slug)
        ).scalar_one_or_none()

        if not source or not source.is_active:
            return {"skipped": True}

        job = CrawlJob(
            source_id=source.id,
            status=CrawlStatus.PENDING,
            triggered_by="schedule",
        )
        session.add(job)
        session.commit()
        execute_crawl_job.delay(str(job.id))
        return {"job_id": str(job.id)}
