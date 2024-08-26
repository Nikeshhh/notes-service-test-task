.PHONY: api
api:
	docker compose -f docker_compose/app.yaml up --build

.PHONY: api-debug
api-debug:
	uvicorn src.main:app --log-level=debug --reload

.PHONY: db
db:
	docker compose -f docker_compose/database.yaml up --build