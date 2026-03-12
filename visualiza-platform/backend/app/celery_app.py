"""
Celery application factory
"""
from celery import Celery

from app.config import settings
from app.crawler.scheduler import CELERY_BEAT_SCHEDULE


def create_celery_app() -> Celery:
    celery_app = Celery(
        "visualiza",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
    )
    celery_app.config_from_object(
        {
            "task_serializer": "json",
            "result_serializer": "json",
            "accept_content": ["json"],
            "timezone": "America/Santo_Domingo",
            "enable_utc": True,
            "beat_schedule": CELERY_BEAT_SCHEDULE,
            "task_routes": {
                "crawler.*": {"queue": "crawl"},
                "billing.*": {"queue": "default"},
            },
        }
    )
    celery_app.autodiscover_tasks(
        ["app.crawler.tasks"]
    )
    return celery_app


celery_app: Celery = create_celery_app()
