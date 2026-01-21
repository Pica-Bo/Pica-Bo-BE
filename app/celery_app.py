# Celery app factory for FastAPI project

# Celery app factory using centralized settings
from celery import Celery
from app.core.config import settings
import scheduler.django_setup 

def make_celery():
	celery = Celery(
		"pica_bo",
		broker=settings.celery_broker_url,
		backend=settings.celery_result_backend,
		include=["app.tasks"]
	)
	celery.conf.update(
		# Serialization and timezone
		task_serializer="json",
		result_serializer="json",
		accept_content=["json"],
		timezone=settings.celery_timezone,
		enable_utc=True,
		# Worker/task reliability and monitoring
		task_acks_late=True,
		worker_prefetch_multiplier=1,
		task_track_started=True,
	)
	celery.conf.beat_scheduler = (
		"django_celery_beat.schedulers:DatabaseScheduler"
		)
	return celery

celery_app = make_celery()
