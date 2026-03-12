"""
Crawler API router (Admin)
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.models.crawler import CrawlJob, CrawlResult, CrawlSource, CrawlStatus
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.crawler import (
    CrawlJobResponse, CrawlResultResponse, CrawlSourceResponse,
    CrawlSourceUpdate, ReviewCrawlResult,
)

router = APIRouter(prefix="/crawler", tags=["Crawler (Admin)"])


@router.get("/sources", response_model=list[CrawlSourceResponse])
async def list_sources(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    result = await db.execute(select(CrawlSource).order_by(CrawlSource.name))
    return result.scalars().all()


@router.put("/sources/{source_id}", response_model=CrawlSourceResponse)
async def update_source(
    source_id: str,
    data: CrawlSourceUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    from app.core.exceptions import NotFoundError
    result = await db.execute(select(CrawlSource).where(CrawlSource.id == source_id))
    source = result.scalar_one_or_none()
    if not source:
        raise NotFoundError("Fuente de rastreo")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(source, key, value)
    await db.flush()
    return source


@router.post("/sources/{source_id}/trigger", response_model=MessageResponse)
async def trigger_crawl(
    source_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    from app.crawler.tasks import execute_crawl_job
    result = await db.execute(select(CrawlSource).where(CrawlSource.id == source_id))
    source = result.scalar_one_or_none()
    if not source:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Fuente de rastreo")

    job = CrawlJob(
        source_id=source_id,
        status=CrawlStatus.PENDING,
        triggered_by="manual",
        triggered_by_user_id=admin.id,
    )
    db.add(job)
    await db.flush()
    execute_crawl_job.delay(str(job.id))
    return MessageResponse(message=f"Rastreo iniciado (job {job.id})")


@router.get("/jobs", response_model=list[CrawlJobResponse])
async def list_jobs(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    result = await db.execute(
        select(CrawlJob).order_by(CrawlJob.created_at.desc()).limit(limit)
    )
    return result.scalars().all()


@router.get("/jobs/{job_id}", response_model=CrawlJobResponse)
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    from app.core.exceptions import NotFoundError
    result = await db.execute(select(CrawlJob).where(CrawlJob.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise NotFoundError("Trabajo de rastreo")
    return job


@router.post("/jobs/{job_id}/cancel", response_model=MessageResponse)
async def cancel_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    from app.core.exceptions import NotFoundError
    result = await db.execute(select(CrawlJob).where(CrawlJob.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise NotFoundError("Trabajo de rastreo")
    if job.status == CrawlStatus.RUNNING:
        job.status = CrawlStatus.CANCELLED
    await db.flush()
    return MessageResponse(message="Trabajo cancelado")


@router.get("/results", response_model=list[CrawlResultResponse])
async def list_pending_results(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    result = await db.execute(
        select(CrawlResult)
        .where(CrawlResult.is_approved.is_(None))
        .order_by(CrawlResult.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


@router.post("/results/{result_id}/approve", response_model=MessageResponse)
async def approve_result(
    result_id: str,
    data: ReviewCrawlResult,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    from app.core.exceptions import NotFoundError
    res = await db.execute(select(CrawlResult).where(CrawlResult.id == result_id))
    crawl_result = res.scalar_one_or_none()
    if not crawl_result:
        raise NotFoundError("Resultado de rastreo")

    crawl_result.is_approved = data.approved
    crawl_result.reviewed_by = admin.id
    crawl_result.review_notes = data.notes

    if data.approved:
        # Create or update product from crawl result
        from app.models.product import Product, ProductStatus, ProductSource
        raw = crawl_result.raw_data
        product = Product(
            name=crawl_result.normalized_name or raw.get("name", ""),
            name_es=raw.get("name_es"),
            sku=crawl_result.source_sku or crawl_result.normalized_name[:50] if crawl_result.normalized_name else "",
            price=crawl_result.normalized_price or 0.0,
            currency=crawl_result.normalized_currency or "DOP",
            slug=f"crawled-{result_id[:8]}",
            source=ProductSource.CRAWLED,
            source_url=crawl_result.source_url,
            status=ProductStatus.ACTIVE,
            images=crawl_result.normalized_images,
            thumbnail_url=crawl_result.normalized_images[0] if crawl_result.normalized_images else None,
            specifications=raw.get("specifications", {}),
            description=raw.get("description"),
            description_es=raw.get("description_es"),
        )
        db.add(product)
        await db.flush()
        crawl_result.product_id = product.id

    await db.flush()
    action = "aprobado" if data.approved else "rechazado"
    return MessageResponse(message=f"Resultado {action}")


@router.post("/results/{result_id}/reject", response_model=MessageResponse)
async def reject_result(
    result_id: str,
    data: ReviewCrawlResult,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    data.approved = False
    return await approve_result(result_id, data, db, admin)
