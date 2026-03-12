"""
Public Widget API — CORS-open, API key authenticated
"""
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.product import Product, ProductStatus
from app.models.visualizer import VisualizerSession
from app.schemas.bom import BomGenerateRequest, BomResponse
from app.services.bom_service import BomService
from app.services.widget_service import WidgetService

router = APIRouter(prefix="/widget", tags=["Widget (Public)"])


class WidgetValidateRequest(BaseModel):
    api_key: str
    origin: str


class WidgetValidateResponse(BaseModel):
    valid: bool
    widget_config: dict | None = None
    reason: str | None = None


@router.post("/validate", response_model=WidgetValidateResponse)
async def validate_widget(
    req: WidgetValidateRequest, db: AsyncSession = Depends(get_db)
):
    result = await WidgetService.validate_widget_access(req.api_key, req.origin, db)
    return result


@router.get("/catalog")
async def widget_catalog(
    api_key: str = Query(...),
    surface_type: str | None = None,
    category: str | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=24, le=48),
    db: AsyncSession = Depends(get_db),
):
    """Public product catalog for the embedded widget."""
    # Validate API key
    from sqlalchemy import select
    from app.models.professional import ProfessionalProfile

    res = await db.execute(
        select(ProfessionalProfile).where(ProfessionalProfile.api_key == api_key)
    )
    if not res.scalar_one_or_none():
        from app.core.exceptions import UnauthorizedError
        raise UnauthorizedError("API key inválida")

    q = select(Product).where(
        Product.status == ProductStatus.ACTIVE,
        Product.is_visualizer_compatible.is_(True),
    )
    if surface_type:
        q = q.where(Product.surface_types.like(f'%"{surface_type}"%'))
    if search:
        q = q.where(Product.name.ilike(f"%{search}%"))

    q = q.offset((page - 1) * limit).limit(limit)
    result = await db.execute(q)
    products = result.scalars().all()

    return {
        "items": [
            {
                "id": str(p.id),
                "name": p.name,
                "name_es": p.name_es,
                "price": p.price,
                "currency": p.currency,
                "price_unit": p.price_unit,
                "thumbnail_url": p.thumbnail_url,
                "texture_url": p.texture_url,
                "surface_types": p.surface_types,
                "brand": {"name": p.brand.name} if p.brand else None,
                "category": {"name": p.category.name_es or p.category.name} if p.category else None,
            }
            for p in products
        ],
        "page": page,
        "limit": limit,
    }


@router.post("/bom/generate", response_model=BomResponse)
async def public_generate_bom(
    api_key: str = Query(...),
    data: BomGenerateRequest = ...,
    db: AsyncSession = Depends(get_db),
):
    """Generate BoM from widget session — validates API key, increments usage."""
    from app.models.professional import ProfessionalProfile
    from app.core.exceptions import UnauthorizedError, PlanLimitError
    from app.models.billing import Subscription, SubscriptionStatus

    res = await db.execute(
        select(ProfessionalProfile).where(ProfessionalProfile.api_key == api_key)
    )
    profile = res.scalar_one_or_none()
    if not profile:
        raise UnauthorizedError()

    # Check plan limits
    sub_res = await db.execute(
        select(Subscription).where(
            Subscription.user_id == profile.user_id,
            Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]),
        )
    )
    sub = sub_res.scalar_one_or_none()
    if sub and sub.bom_exports_used >= sub.plan.max_bom_exports_per_month:
        raise PlanLimitError()

    bom = await BomService.generate_bom(data, db, professional_id=str(profile.id))

    if sub:
        sub.bom_exports_used += 1
        await db.flush()

    return bom


@router.post("/session")
async def create_session(
    api_key: str = Query(...),
    room_image_url: str | None = None,
    property_url: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Create a new visualizer session for widget."""
    from app.models.professional import ProfessionalProfile
    from app.core.exceptions import UnauthorizedError

    res = await db.execute(
        select(ProfessionalProfile).where(ProfessionalProfile.api_key == api_key)
    )
    profile = res.scalar_one_or_none()
    if not profile:
        raise UnauthorizedError()

    session = VisualizerSession(
        professional_id=profile.id,
        room_image_url=room_image_url,
        widget_api_key=api_key,
        property_url=property_url,
    )
    db.add(session)
    await db.flush()
    return {"session_id": str(session.id)}
