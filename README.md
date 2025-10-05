# Spy Cat Agency Backend

This is the backend for the Spy Cat Agency (SCA) management system.
It is built with **Django + Django REST Framework**, using **SQLite** as the database.

The backend exposes CRUD APIs for:
- Spy Cats
- Missions
- Targets

---

## Features

### Cats
- Create, read, update (salary only), delete spy cats
- Breed validation (optional integration with TheCatAPI)

### Missions
- Create missions with targets in one request
- Assign cats to missions
- Auto-complete mission when all targets are completed
- Cannot delete mission if assigned to a cat

### Targets
- Update notes (restricted if mission/target completed)
- Mark as completed

---

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite
- Docker & Docker Compose

---

## Project Structure

```
spycat-backend/
├─ spycat-be/
│ ├─ spycat_be/
│ ├─ cats/
│ ├─ integrations/
│ ├─ missions/
│ └─ manage.py
├─ docker/
│ └─ django/Dockerfile
├─ docker-compose.yml
├─ .env
├─ README.md
└─ .gitignore
```

---

## Setup & Run (Docker)

```bash
git clone <repo-url>
cd spycat-backend
cp .env.example .env
docker network create spycat-network
docker compose up --build
docker compose exec web python manage.py migrate
```

## API Endpoints

### Cats
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/cats/` | List all cats |
| GET | `/api/cats/{id}/` | Retrieve single cat |
| POST | `/api/cats/` | Create a cat |
| PATCH | `/api/cats/{id}/` | Update cat salary |
| DELETE | `/api/cats/{id}/` | Delete cat |

### Missions
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/missions/` | List missions |
| GET | `/api/missions/{id}/` | Retrieve single mission |
| POST | `/api/missions/` | Create mission with targets |
| PATCH | `/api/missions/{id}/` | Assign cat |
| DELETE | `/api/missions/{id}/` | Delete mission (only if no cat assigned) |

### Targets
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/targets/` | List targets |
| GET | `/api/targets/{id}/` | Retrieve single target |
| PATCH | `/api/targets/{id}/` | Update notes or mark completed |

---

## Postman Collection

[Try endpoints here](https://www.postman.com/joint-operations-astronomer-9341736/spycat-be/collection/lmlktaj/cats)

