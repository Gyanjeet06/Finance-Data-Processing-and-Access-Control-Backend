# Finance Data Processing and Access Control Backend

A robust RESTful API backend for a finance dashboard system, implementing role-based access control (RBAC), financial record management, and dashboard analytics aggregation. Built with FastAPI, SQLAlchemy, and SQLite.

---

## Architecture

The project follows a layered architectural pattern to enforce separation of concerns, maintainability, and scalability.

| Layer | Path | Responsibility |
| :---- | :---- | :---- |
| API | `app/api/` | Route controllers and dependency injection, separated by domain (auth, users, records, stats) |
| CRUD | `app/crud/` | All database interactions and business logic, keeping the API layer thin and testable |
| Models | `app/models/` | SQLAlchemy ORM models defining the database schema |
| Schemas | `app/schemas/` | Pydantic models for request/response validation and serialization |
| Core | `app/core/` | Configuration management and security utilities (JWT, password hashing) |
| DB | `app/db/` | Database session management and base classes |

---

## Directory Structure

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/       # Route handlers per domain (auth, users, records, stats)
│   ├── core/                    # JWT utilities, password hashing, config
│   ├── crud/                    # Database interaction and business logic
│   ├── db/                      # Session management and declarative base
│   ├── models/                  # SQLAlchemy ORM models
│   ├── schemas/                 # Pydantic request/response schemas
│   └── main.py                  # Application entry point
├── tests/                       # Pytest test suite
├── .env                         # Environment variables (not committed)
├── requirements.txt
└── README.md
```

---

## Core Features

### 1. User and Role Management

Authentication is handled via JWT (OAuth2) with bcrypt-hashed passwords. Three roles are enforced:

- **viewer** — Access to dashboard summaries and trends only.
- **analyst** — Can view financial records plus all viewer permissions.
- **admin** — Full CRUD access to all users and financial records.

New users register with the `viewer` role by default to ensure safe onboarding.

### 2. Financial Records Management

Full CRUD endpoints for managing financial entries (`income` / `expense`), with native query parameter filtering by `category`, `entry_type`, `start_date`, and `end_date`.

### 3. Dashboard Summary APIs

Aggregation logic is handled at the CRUD layer to minimize memory overhead.

- `GET /api/v1/stats/summary` — Returns total income, total expenses, net balance, category-wise totals, and recent activity.
- `GET /api/v1/stats/trends` — Returns grouped monthly trend analysis.

### 4. Access Control

Enforced via FastAPI Dependency Injection using a `require_roles` guard in `app/api/deps.py`. This acts as a centralized policy check — if a user's role is not in the allowed list, a `403 Forbidden` is raised before any route logic executes.

### 5. Validation and Error Handling

Pydantic enforces strict input validation (e.g., `entry_type` is constrained to `"income"` or `"expense"` via `Literal`). Custom HTTP exceptions are raised for business logic errors such as `404 Not Found` for missing records and `400 Bad Request` for duplicate emails.

### 6. Data Persistence

SQLite via SQLAlchemy was chosen for zero-configuration setup. A one-to-many relationship exists between `User` and `Record`, with cascading deletes to prevent orphaned records when a user is removed.

---

## Setup and Installation

### Prerequisites

Python 3.10 or higher.

### Step 1 — Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./finance.db
SECRET_KEY=your_super_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Step 4 — Run the Application

```bash
uvicorn app.main:app --reload --port 8000
```

Interactive API documentation will be available at `http://localhost:8000/docs`.

### Step 5 — Run Tests

```bash
pytest
```

---

## API Reference

| Method | Endpoint | Role Required | Description |
| :---- | :---- | :---- | :---- |
| POST | `/api/v1/auth/token` | Public | Authenticate and receive a JWT |
| POST | `/api/v1/users/` | Public | Register a new user (defaults to viewer) |
| GET | `/api/v1/users/me` | Any authenticated | Get the current user's profile |
| GET | `/api/v1/users/` | admin | List all users in the system |
| PATCH | `/api/v1/users/{id}` | admin | Update a user's role or active status |
| POST | `/api/v1/records/` | admin | Create a financial record |
| GET | `/api/v1/records/` | analyst, admin | List and filter financial records |
| PUT | `/api/v1/records/{id}` | admin | Update a specific record |
| DELETE | `/api/v1/records/{id}` | admin | Delete a specific record |
| GET | `/api/v1/stats/summary` | viewer, analyst, admin | Get dashboard KPIs and recent activity |
| GET | `/api/v1/stats/trends` | analyst, admin | Get monthly income/expense trends |

---

## Assumptions and Trade-offs

**Database choice.** SQLite was chosen for immediate evaluability. Because the project uses SQLAlchemy, switching to PostgreSQL in a production environment requires only updating `DATABASE_URL` and installing `psycopg2` or `asyncpg` — no application code changes needed.

**In-memory aggregation.** Dashboard aggregations currently fetch records and aggregate in Python. For a production system at scale, these would be pushed to the database using `GROUP BY` SQL queries to reduce memory overhead.

**Hard deletes.** Physical deletes were used to keep the implementation focused. A real-world financial system would use soft deletes (an `is_deleted` boolean flag) for audit trail and compliance purposes.

---

## Potential Improvements

- **Dockerization** — Wrap the application and a PostgreSQL instance in a `docker-compose.yml` for reproducible, isolated deployments.
- **Pagination** — Add `limit` and `offset` parameters to `GET /records/` to handle large datasets.
- **Caching** — Use Redis to cache responses from `/stats/summary` and `/stats/trends`, since dashboard data is read-heavy and infrequently mutated.