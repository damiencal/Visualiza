"""
Billing router
"""
from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_professional, get_db
from app.models.user import User
from app.models.professional import ProfessionalProfile
from app.schemas.billing import (
    CheckoutRequest, CheckoutResponse, CustomerPortalRequest,
    CustomerPortalResponse, PlanResponse, SubscriptionResponse, UsageResponse,
)
from app.services.billing_service import BillingService

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.get("/plans", response_model=list[PlanResponse])
async def list_plans(db: AsyncSession = Depends(get_db)):
    return await BillingService.list_plans(db)


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    data: CheckoutRequest,
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    user, _ = auth
    return await BillingService.create_checkout_session(user, data, db)


@router.post("/portal", response_model=CustomerPortalResponse)
async def customer_portal(
    data: CustomerPortalRequest,
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    user, _ = auth
    url = await BillingService.create_customer_portal(user, data.return_url, db)
    return CustomerPortalResponse(portal_url=url)


@router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="stripe-signature"),
    db: AsyncSession = Depends(get_db),
):
    if not stripe_signature:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Missing Stripe signature")
    payload = await request.body()
    return await BillingService.handle_webhook(payload, stripe_signature, db)
