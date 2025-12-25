.PHONY: dev api test fmt lint

dev:
	docker compose up --build

api:
	uvicorn swat_copilot.api.app:create_app --factory --reload

test:
	pytest -q

fmt:
	ruff check --fix .
	black .

lint:
	ruff check .
	mypy src
