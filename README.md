# Сервис для работы с заметками
Репозиторий содержит решение тестового задания от компании KODE.

Сервис предоставляет возможность создания и просмотра заметок для пользователя. При создании заметок используется валидация слов при помощи `Яндекс.Спеллер`.

Для создания приложения используются следующие технологии:
* FastAPI
* Poetry
* SQLAlchemy
* Alembic
* Pytest
* HTTPX
* `Яндекс.Спеллер`
* Docker
* Make

Файловая структура вдохновлена этим репозиторием: `https://github.com/zhanymkanov/fastapi-best-practices`

Для тестирования приложения были написаны тесты а также коллекция Postman.

 [<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/28326301-9a66320e-66a4-4b50-9326-e3d7fc9f36b7?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D28326301-9a66320e-66a4-4b50-9326-e3d7fc9f36b7%26entityType%3Dcollection%26workspaceId%3Da7efa347-e352-4a73-abe5-a2939500163f)


## Содержание

- [Сервис для работы с заметками](#сервис-для-работы-с-заметками)
  - [Содержание](#содержание)
  - [Запуск приложения](#запуск-приложения)
    - [В докере](#в-докере)
    - [Локально](#локально)


## Запуск приложения

Клонировать репозиторий:
```
git clone https://github.com/Nikeshhh/notes-service-test-task.git
```
или
```
git clone git@github.com:Nikeshhh/notes-service-test-task.git
```

### В докере

Создать файл виртуального окружения `.env`:
```
cat .env.example >> .env
```

Запустить контейнеры:
```
make app
```
или
```
docker compose -f docker_compose/database.yaml -f docker_compose/app.yaml up --build
```

Создать тестовую базу данных:
```
make create_test_db
```
или
```
docker exec -it db psql -U postgresql -d notesdb -c "CREATE DATABASE testdb"
```

Запустить тесты:
```
make test
```
или
```
docker exec -it main-app poetry run pytest -vv /tests/
```

### Локально

Создать файл виртуального окружения `.env`:
```
cat .env.example >> .env
```

Заккоментировать, удалить или изменить переменную `POSTGRES_HOST` на `localhost`:
```
# POSTGRES_HOST=postgres_notes
```
или
```
POSTGRES_HOST=localhost
```

Изменить порт, если стандартный порт `5432` у вас занят:
```
POSTGRES_PORT=5431
```

Запустить базу данных в контейнере:
```
make db
```
или
```
docker compose -f docker_compose/database.yaml up --build
```

Запустить uvicorn:
```
make api-debug
```
или
```
uvicorn src.main:app --log-level=debug --reload
```

Создать тестовую базу данных:
```
make create_test_db
```
или
```
docker exec -it db psql -U postgresql -d notesdb -c "CREATE DATABASE testdb"
```

Запустить тесты:
```
pytest -vv /tests/
```