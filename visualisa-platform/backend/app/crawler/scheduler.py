"""
Celery Beat schedule configuration
"""
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # Aliss: every Monday at 3 AM
    "crawl-aliss-weekly": {
        "task": "crawler.scheduled_crawl",
        "schedule": crontab(hour=3, minute=0, day_of_week=1),
        "args": ("aliss",),
    },
    # Ochoa: every Wednesday at 3 AM
    "crawl-ochoa-weekly": {
        "task": "crawler.scheduled_crawl",
        "schedule": crontab(hour=3, minute=0, day_of_week=3),
        "args": ("ochoa",),
    },
    # IKEA DR: every Friday at 3 AM
    "crawl-ikea-dr-weekly": {
        "task": "crawler.scheduled_crawl",
        "schedule": crontab(hour=3, minute=0, day_of_week=5),
        "args": ("ikea-dr",),
    },
    # Reset daily API call counters at midnight UTC
    "reset-api-call-counters-daily": {
        "task": "billing.reset_api_counters",
        "schedule": crontab(hour=0, minute=0),
    },
}
