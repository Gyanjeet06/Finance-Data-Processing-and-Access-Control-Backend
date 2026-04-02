# Finance Data Processing and Access Control Backend

A FastAPI backend implementation for a finance dashboard system with role-based access control, financial record management, and dashboard analytics.

## What is included

- User management with roles: `viewer`, `analyst`, and `admin`
- JWT authentication for secure API access
- Financial record CRUD operations
- Dashboard summary and trends endpoints
- SQLite persistence via SQLAlchemy
- Input validation and error handling with Pydantic

## Project layout

- `app/main.py` - FastAPI application entrypoint
- `app/api/` - API router definitions and dependencies
- `app/api/v1/endpoints/` - Versioned route implementations
- `app/core/` - Configuration and security utilities
- `app/crud/` - Database logic and business operations
- `app/models/` - SQLAlchemy ORM models
- `app/schemas/` - Pydantic request/response schemas
- `app/db/` - Database session and schema initialization
- `tests/` - Basic smoke test suite

## API overview

- `POST /api/v1/auth/token` - Login and receive access token
- `POST /api/v1/users/` - Register a new viewer user
- `GET /api/v1/users/me` - Get current authenticated user
- `GET /api/v1/users/` - List all users (admin only)
- `PATCH /api/v1/users/{user_id}` - Update user role/status (admin only)
- `POST /api/v1/records/` - Create a financial record (admin only)
- `GET /api/v1/records/` - List records (analyst/admin)
- `GET /api/v1/records/{record_id}` - Get one record (analyst/admin)
- `PUT /api/v1/records/{record_id}` - Update a record (admin only)
- `DELETE /api/v1/records/{record_id}` - Delete a record (admin only)
- `GET /api/v1/stats/summary` - Dashboard summary (viewer+)
- `GET /api/v1/stats/trends` - Monthly trends (analyst/admin)

## Setup

1. Create a Python environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env` with the following values

```env
DATABASE_URL=sqlite:///./finance.db
SECRET_KEY=replace_with_a_secure_key
```

4. Start the application

```bash
uvicorn app.main:app --reload --port 8000
```

## Notes

- The backend uses SQLite for persistence and automatically creates tables on startup.
- Role-based access control is enforced in dependency middleware.
- Open user registration creates a `viewer` by default.
- Authentication works with Bearer tokens issued at `/api/v1/auth/token`.
