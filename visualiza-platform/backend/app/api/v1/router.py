"""
V1 Router — aggregates all v1 sub-routers
"""
from fastapi import APIRouter

from .auth import router as auth_router
from .billing import router as billing_router
from .bom import router as bom_router
from .crawler import router as crawler_router
from .products import brands_router, categories_router, router as products_router
from .professional import router as professional_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(products_router)
api_router.include_router(brands_router)
api_router.include_router(categories_router)
api_router.include_router(crawler_router)
api_router.include_router(bom_router)
api_router.include_router(billing_router)
api_router.include_router(professional_router)
