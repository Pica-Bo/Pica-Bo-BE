# Example Celery task
from app.celery_app import celery_app

@celery_app.task(bind=True)
def debug_task(self):
	print(f'Request: {self.request!r}')

# Example periodic task (if using django-celery-beat, schedule via Django admin)

