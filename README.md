# Travel Planner API
A management application for planning trips with artworks from the **Art Institute of Chicago API**.
Built with **FastAPI**, **SQLAlchemy**, **SQLite**.

## Quick Start
```bash
git clone <repo-url>
cd Travel_planner
docker compose up --build
```
The API will be available at `http://localhost:8000`.

**Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints
| Method | URL | Description |
|-------|-----|----------|
| `GET` | `/api/v1/artworks/search?title=...` | Search artworks in the Art Institute of Chicago |
| `POST` | `/api/v1/projects` | Create a project (with or without places) |
| `GET` | `/api/v1/projects` | List projects |
| `GET` | `/api/v1/projects/{id}` | Get a project |
| `PATCH` | `/api/v1/projects/{id}` | Update a project |
| `DELETE` | `/api/v1/projects/{id}` | Delete a project |
| `POST` | `/api/v1/projects/{id}/places` | Add a place (artwork) |
| `GET` | `/api/v1/projects/{id}/places` | List places |
| `PATCH` | `/api/v1/projects/{id}/places/{place_id}` | Update a place (notes/visited) |

## Postman
Import `travel_planner.postman_collection.json` into Postman.
