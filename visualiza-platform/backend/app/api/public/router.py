"""
Public router — widget API + catalog
"""
from fastapi import APIRouter

from .widget_api import router as widget_router

public_router = APIRouter()
public_router.include_router(widget_router)
