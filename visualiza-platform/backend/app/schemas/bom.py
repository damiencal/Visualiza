"""
Bill of Materials schemas
"""
from pydantic import BaseModel, Field


class BomLineItemRequest(BaseModel):
    product_id: str
    surface_type: str
    quantity: float = Field(gt=0)
    unit: str
    wastage_percent: float = 10.0
    notes: str | None = None


class BomGenerateRequest(BaseModel):
    room_type: str
    room_image_url: str | None = None
    measurements: dict
    # {"floor_area_m2": 25.5, "wall_area_m2": 48.0, "ceiling_area_m2": 25.5}
    line_items: list[BomLineItemRequest]
    notes: str | None = None
    session_id: str | None = None


class BomLineItemResponse(BaseModel):
    id: str
    product_id: str
    surface_type: str
    quantity: float
    unit: str
    unit_price: float
    line_total: float
    wastage_percent: float
    quantity_with_wastage: float
    notes: str | None = None
    product: dict | None = None  # embedded product summary
    model_config = {"from_attributes": True}


class BomResponse(BaseModel):
    id: str
    room_type: str
    room_image_url: str | None = None
    rendered_image_url: str | None = None
    measurements: dict
    subtotal: float
    tax_rate: float
    tax_amount: float
    total: float
    currency: str
    notes: str | None = None
    is_shared: bool
    share_token: str | None = None
    line_items: list[BomLineItemResponse] = []
    model_config = {"from_attributes": True}


class BomShareResponse(BaseModel):
    share_url: str
    share_token: str
