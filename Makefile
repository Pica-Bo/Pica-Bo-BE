# Run django-celery-beat scheduler with Django ORM scheduler
django-celery-beat:
	celery -A app.celery_app.celery_app beat -S django -l info
celery-worker:
	celery -A app.celery_app.celery_app worker --loglevel=info

celery-beat:
	celery -A app.celery_app.celery_app beat --loglevel=info

flower:
	celery -A app.celery_app.celery_app flower --port=5555

.PHONY: up build run test lint

up:
	docker-compose up --build

build:
	docker-compose build

run:
	uv run -m uvicorn app.main:app --reload

lint:
	pylint app

test:
	pytest -q
