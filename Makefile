.PHONY: api
api:
	docker compose -f docker_compose/app.yaml up --build

.PHONY: api-debug
api-debug:
	uvicorn src.main:app --log-level=debug --reload

.PHONY: db
db:
	docker compose -f docker_compose/database.yaml up --build

.PHONY: app
app:
	docker compose -f docker_compose/database.yaml -f docker_compose/app.yaml up --build

.PHONY: test
test:
	docker exec -it main-app poetry run pytest -vv /tests/

.PHONY: create_test_db
create_test_db:
	docker exec -it db psql -U postgresql -d notesdb -c "CREATE DATABASE testdb"