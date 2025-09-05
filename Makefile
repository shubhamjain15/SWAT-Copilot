.PHONY: dev api test fmt lint
dev:
docker compose up --build
api:
uvicorn swat_copilot.api.main:app --reload
test:
pytest -q
fmt:
ruff check --fix .
black .
lint:
ruff check .
mypy src
