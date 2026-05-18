## Tasks

### 1. Project scaffolding
- [x] Move `main.py` → `app/main.py` and refactor to use `app` layout
- [x] Create `app/__init__.py`
- [x] Create `app/database.py` with SQLite engine + session dependency
- [x] Create `app/models/__init__.py`
- [x] Create `app/routes/__init__.py`
- [x] Create `app/services/__init__.py`
- [x] Create `app/repositories/__init__.py`

### 2. Models (sqlmodel)
- [x] Create `models/application.py`:
  - `ApplicationStatus` enum
  - `Application` table model
  - `ApplicationCreate` / `ApplicationUpdate` schemas
  - `ApplicationPublic` response model
- [x] Create `models/interview.py`:
  - `InterviewType` enum
  - `Interview` table model (with FK to application, cascade delete)
  - `InterviewCreate` / `InterviewUpdate` schemas
  - `InterviewPublic` response model

### 3. Repositories
- [x] Create `repositories/application_repository.py`:
  - `create`, `get_by_id`, `list_all` (with optional filters), `update`, `delete`
  - `get_status_summary` — group by status with counts
- [x] Create `repositories/interview_repository.py`:
  - `create`, `get_by_id` (scoped to application), `list_for_application`, `update`, `delete`
  - `create`, `get_by_id` (scoped to application), `list_for_application`, `update`, `delete`

### 4. Services
- [x] Create `services/application_service.py`:
  - CRUD delegation to repository
  - Status transition validation (state machine rules)
  - Summary computation
- [x] Create `services/interview_service.py`:
  - CRUD delegation to repository
  - Scoped to parent application existence checks
  - CRUD delegation to repository
  - Scoped to parent application existence checks

### 5. Routes
- [x] Create `routes/applications.py`:
  - `POST /applications` → create
  - `GET /applications` → list with filters
  - `GET /applications/{id}` → get by ID
  - `PATCH /applications/{id}` → update (partial)
  - `DELETE /applications/{id}` → delete
  - `GET /applications/summary` → status counts
- [x] Create `routes/interviews.py`:
  - `POST /applications/{id}/interviews` → create
  - `GET /applications/{id}/interviews` → list for application
  - `GET /applications/{id}/interviews/{interview_id}` → get by ID
  - `PATCH /applications/{id}/interviews/{interview_id}` → update
  - `DELETE /applications/{id}/interviews/{interview_id}` → delete
- [x] Create `routes/test.py`:
  - `GET /health` → 200 OK
  - `POST /test/reset` → truncate all tables

### 6. Main application
- [x] Update `app/main.py`:
  - Create FastAPI app with lifespan
  - Include all routers
  - Create tables on startup (dev convenience)

### 7. Alembic migrations
- [x] Initialize Alembic: `alembic init alembic`
- [x] Configure `alembic.ini` to use SQLite URL
- [x] Configure `env.py` to use sqlmodel metadata
- [x] Generate initial migration: `alembic revision --autogenerate -m "initial"`
- [x] Apply migration: `alembic upgrade head`

### 8. Verification
- [x] Run BDD tests: `uv run behave` → all 65 scenarios pass
- [x] All scenarios from `applications.feature`, `interviews.feature`, `application_status.feature` pass
- [x] Test summary endpoint returns correct counts
- [x] Test cascade delete (deleting application removes interviews)
- [x] Test state machine validation (invalid transitions return 422)
