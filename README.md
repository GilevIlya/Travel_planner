# Travel Planner API

A management application for planning trips with artworks from the **Art Institute of Chicago API**.

Built with **FastAPI**, **SQLAlchemy**, **SQLite**.

## Quick Start

```bash
git clone <repo-url>
cd travel-planner
docker compose up --build
```

API будет доступен на `http://localhost:8000`.

**Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/api/v1/artworks/search?title=...` | Поиск картин в Art Institute Chicago |
| `POST` | `/api/v1/projects` | Создать проект (c местами или без) |
| `GET` | `/api/v1/projects` | Список проектов |
| `GET` | `/api/v1/projects/{id}` | Получить проект |
| `PATCH` | `/api/v1/projects/{id}` | Обновить проект |
| `DELETE` | `/api/v1/projects/{id}` | Удалить проект |
| `POST` | `/api/v1/projects/{id}/places` | Добавить место (artwork) |
| `GET` | `/api/v1/projects/{id}/places` | Список мест |
| `PATCH` | `/api/v1/projects/{id}/places/{place_id}` | Обновить место (notes/visited) |

## Postman

Импортируй `travel_planner.postman_collection.json` в Postman.