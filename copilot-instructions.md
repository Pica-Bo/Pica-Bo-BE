# Copilot Architecture & Coding Instructions

These instructions are for GitHub Copilot (and similar AI assistants) when working on this backend.

## 1. Tooling & Dependencies

- **Python & environment**
  - Target Python: **3.11+** (see `requires-python` in `pyproject.toml`).
  - Use **uv** as the primary tool for dependency management in Docker and CI.
- **pyproject.toml**
  - This project uses a **PEP 621 `[project]`** section, **not** `[tool.poetry]`.
  - The build backend is **hatchling**:
    - Do **not** reintroduce Poetry or `[tool.poetry]`.
  - When adding dependencies:
    - Add them to `[project].dependencies`.
    - Add dev-only tools to `[dependency-groups].dev`.
- **Installing dependencies with uv**
  - In Docker and scripts, prefer:
    - `uv pip install . --system`
  - Do **not** manually duplicate dependency lists in the Dockerfile; always rely on `pyproject.toml`.

## 2. Docker & Compose

- **Dockerfile**
  - Base image: `python:3.11-slim`.
  - Pattern:
    1. `COPY pyproject.toml ./`
    2. `RUN pip install --upgrade pip && pip install uv && uv pip install . --system`
    3. `COPY . .`
    4. `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]`
  - Do **not** introduce extra venvs in Docker; the container uses the system environment.
- **docker-compose.yml**
  - Service name: `backend`, container name: `pb-backend`.
  - Ports: `8000:8000`.
  - Mongo and Redis are defined as services and should continue to be used.
  - Environment variables for `backend` are set **inline** under `environment:` (not via `env_file`), and must match `app.core.config.Settings` fields.
  - It is acceptable to keep a `./:/usr/src/app` volume for local development.
  - `docker compose watch` is **not required**; no `develop` section is needed unless explicitly requested.

## 3. Data Models & Beanie

- Beanie documents live under `app/models/`.
- Common imports (from `app/models/__init__.py`) should be reused instead of redefining types.
- **User model** (`app/models/user.py`):
  - Represents an **operator profile only**, **not** authentication data.
  - Fields (current canonical shape):
    - `email: Indexed(str, unique=True)`
    - `full_name: str`
    - Optional profile fields: `profile_image_url`, `preferred_language`, `timezone`, `phone`, `country`.
    - `status: str = "active"`
    - `created_at: datetime = Field(default_factory=datetime.utcnow)`
  - Do **not** add `password`, `password_hash`, `role`, or any other auth/credential fields to this model.
- **Placeholders**
  - Placeholder models under `app/models/placeholders` have been removed on purpose.
  - Do **not** recreate or depend on placeholder models; always use real models under `app/models/`.

## 4. Authentication & Authorization

- This service **does not implement authentication or password management**.
- Rules:
  - Do **not** store passwords, password hashes, tokens, or auth roles in any collection.
  - Do **not** reintroduce password hashing utilities (`passlib`, `CryptContext`) for user data.
  - The `/auth` router currently only returns a `501 Not Implemented` stub indicating that auth is handled elsewhere. Do **not** implement a full login/registration flow here unless explicitly requested.

## 5. Application Structure & Patterns

- **Layering**
  - Models: `app/models/*` (Beanie documents only).
  - Repositories: `app/repositories/*` (CRUD operations around Beanie models).
  - Services: `app/services/*` (business logic, built on repositories, subclass `BaseService`).
  - Schemas (Pydantic): `app/schemas/*` (request/response DTOs).
  - Routers: `app/api/routers/*` (FastAPI endpoints using services + schemas).
- **Repository pattern**
  - Follow the existing pattern from `ActivityRepository` and `TeamMemberRepository`:
    - Use `PydanticObjectId` for lookups by string id.
    - Implement `get`, `list`, `create`, `update`, `delete`.
- **Service pattern**
  - Inherit from `BaseService` to use `_not_found`, `_bad_request`, etc.
  - Expose high-level methods like `create_x`, `update_x` and convert models to schemas via a private `_to_schema` method.
- **Router pattern**
  - Use `APIRouter` with dependency-injected service singletons, mirroring `activity` and `team_member` routers.
  - Keep endpoints resource-oriented (`/users`, `/teams`, etc.).

## 6. User CRUD Guidelines

- User CRUD is operator-focused and must:
  - Use `User` (profile model) as the backing Beanie document.
  - Use `UserRepository`, `UserService`, and the `/users` router that already exist.
  - Only manipulate profile fields (email, name, contact, status, etc.).
- When extending user functionality:
  - Add new optional profile fields if needed (e.g., `job_title`), but keep them non-auth.
  - Update schemas in `app/schemas/user.py`, then adjust `UserService._to_schema` accordingly.

## 7. Database Migrations

- **Migration system**
  - Migrations live under `app/migrations/versions/`.
  - Each migration must:
    - Inherit from `BaseMigration` (from `app/migrations`).
    - Implement a unique `name` property (e.g., `"001_create_user_indexes"`).
    - Implement an `up(client)` method for applying changes.
    - Optionally implement `down(client)` for rollback.
  - Register all migrations in `app/migrations/registry.MIGRATIONS` in order.
- **Running migrations**
  - Migrations run **automatically on app startup** via `app/core/db_init.py`.
  - Manual CLI tool: `python -m app.migrations.cli migrate` or `python -m app.migrations.cli status`.
  - Migration state is tracked in a `migrations_log` collection.
- **Creating new migrations**
  - Name files like `XXX_description.py` where `XXX` is a sequential number.
  - Import and add the migration instance to `MIGRATIONS` in `app/migrations/registry.py`.
  - Migrations run in list order; do **not** reorder or rename completed migrations.
- **Examples**
  - Index creation: see `001_create_user_indexes.py`.
  - Data transformations: use the same pattern, accessing collections via `client.get_default_database()["collection_name"]`.

## 8. Error Handling

- Use `BaseService` helpers to raise domain errors instead of FastAPI HTTPException directly from services.
- Routers should generally delegate error creation to services.

## 9. General Copilot Behavior

- Before making structural or tooling changes, **check this file** and prefer to:
  - Reuse existing patterns (repository/service/router) instead of inventing new ones.
  - Keep changes minimal and focused on the requested feature.
- Do **not**:
  - Switch back to Poetry or modify `pyproject.toml` away from the current `[project]` + `hatchling` setup without an explicit request.
  - Add password-based auth, roles, or any credential storage unless the user clearly asks for it.
  - Introduce new top-level services or directories that do not fit the existing layout.

If a future team member requests changes that conflict with these rules (e.g., adding password storage), Copilot should explicitly call out the conflict and ask for confirmation before proceeding.
