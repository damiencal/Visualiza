"""
Widget / Professional Portal schemas
"""
from pydantic import BaseModel, Field


class WidgetConfigUpdate(BaseModel):
    button_text: str | None = Field(default=None, max_length=50)
    button_position: str | None = None
    accent_color: str | None = None
    custom_css: str | None = None
    image_selector: str | None = None


class WidgetDeploymentCreate(BaseModel):
    domain: str = Field(max_length=255)
    button_text: str = "Redecorar"
    button_position: str = "bottom-right"
    custom_css: str | None = None


class WidgetDeploymentResponse(BaseModel):
    id: str
    domain: str
    is_active: bool
    button_text: str
    button_position: str
    custom_css: str | None = None
    model_config = {"from_attributes": True}


class EmbedCodeResponse(BaseModel):
    snippet: str
    api_key: str


class ProfessionalProfileResponse(BaseModel):
    id: str
    user_id: str
    professional_type: str
    company_name: str
    company_website: str | None = None
    license_number: str | None = None
    city: str
    province: str
    country: str
    bio: str | None = None
    logo_url: str | None = None
    api_key: str
    widget_config: dict | None = None
    model_config = {"from_attributes": True}


class ProfessionalProfileUpdate(BaseModel):
    company_name: str | None = None
    company_website: str | None = None
    license_number: str | None = None
    city: str | None = None
    province: str | None = None
    bio: str | None = None
    logo_url: str | None = None


class AnalyticsSummary(BaseModel):
    total_visualizations: int
    total_bom_exports: int
    total_bom_value_dop: float
    top_categories: list[dict]
    visualizations_by_day: list[dict]
