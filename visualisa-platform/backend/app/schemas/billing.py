"""
Billing schemas: Plan, Subscription, Checkout
"""
from datetime import datetime

from pydantic import BaseModel


class PlanResponse(BaseModel):
    id: str
    name: str
    name_es: str
    tier: str
    description: str | None = None
    description_es: str | None = None
    price_monthly_usd: float
    price_yearly_usd: float
    max_visualisations_per_month: int
    max_bom_exports_per_month: int
    max_domains: int
    max_api_calls_per_day: int
    includes_analytics: bool
    includes_custom_branding: bool
    includes_priority_support: bool
    features: list
    sort_order: int
    model_config = {"from_attributes": True}


class SubscriptionResponse(BaseModel):
    id: str
    plan: PlanResponse
    status: str
    billing_cycle: str
    visualisations_used: int
    bom_exports_used: int
    api_calls_today: int
    current_period_start: datetime
    current_period_end: datetime
    trial_end: datetime | None = None
    cancelled_at: datetime | None = None
    model_config = {"from_attributes": True}


class CheckoutRequest(BaseModel):
    plan_id: str
    billing_cycle: str  # "monthly" | "yearly"
    success_url: str
    cancel_url: str


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


class CustomerPortalRequest(BaseModel):
    return_url: str


class CustomerPortalResponse(BaseModel):
    portal_url: str


class UsageResponse(BaseModel):
    visualisations_used: int
    visualisations_limit: int
    bom_exports_used: int
    bom_exports_limit: int
    api_calls_today: int
    api_calls_limit: int
    period_end: datetime
