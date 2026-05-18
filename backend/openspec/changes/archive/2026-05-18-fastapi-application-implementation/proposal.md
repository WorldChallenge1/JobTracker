## Feature-based FastAPI Application Implementation

### What

Build the full FastAPI backend application for the Job Tracker, driven by the existing BDD feature files under `features/`. The application will provide a REST API for managing job applications, their status transitions, and associated interviews.

### Why

The project currently has:
- A stub `main.py` with a single hello-world endpoint
- BDD feature files (`applications.feature`, `interviews.feature`, `application_status.feature`) that specify full behavioral requirements
- Step definitions in `features/steps/` that test against a running API

There is no application code behind these tests yet. This change implements the API so that all BDD scenarios pass.

### Scope

**In scope:**
- SQLite database with sqlmodel ORM
- Application CRUD (create, read, update, delete) with filtering and pagination
- Interview CRUD nested under applications
- Application status state machine with validated transitions
- Status summary endpoint (counts grouped by status)
- Alembic migrations for schema management
- Layered architecture: routes → services → repositories
- Test-specific endpoints (`/test/reset`, `/health`)
- Cascade delete of interviews when an application is deleted

**Out of scope:**
- Authentication / authorization
- Frontend / UI
- Production deployment configuration
- External API integrations
- Reporting beyond status summary
