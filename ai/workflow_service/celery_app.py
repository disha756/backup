from celery import Celery

celery = Celery(
    "workflow",
    broker="redis://localhost:6379/0",
)