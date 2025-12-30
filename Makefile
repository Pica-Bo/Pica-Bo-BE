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
