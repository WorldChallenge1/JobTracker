## Design

### Architecture

Layered architecture following FastAPI best practices:

```
src/app/
├── main.py                  # FastAPI app creation, router mounting, lifespan
├── database.py              # SQLite engine, Session dependency
├── models/
│   ├── __init__.py
│   ├── application.py       # Application sqlmodel + enums
│   └── interview.py         # Interview sqlmodel + enums
├── routes/
│   ├── __init__.py
│   ├── applications.py      # /applications endpoints
│   ├── interviews.py        # /applications/{id}/interviews endpoints
│   └── test.py              # /test/reset, /health endpoints
├── services/
│   ├── __init__.py
│   ├── application_service.py  # Business logic for applications
│   └── interview_service.py    # Business logic for interviews
└── repositories/
    ├── __init__.py
    ├── application_repository.py  # DB queries for applications
    └── interview_repository.py    # DB queries for interviews
```

### Database

- **Engine**: SQLite via sqlmodel (`sqlite+aiosqlite` or synchronous `sqlite:///./jobtracker.db`)
- **Migration**: Alembic with auto-generation
- **Test reset**: truncate all tables via raw SQL
- **Lifespan**: create tables on startup for dev (Alembic for production)

### Models

**ApplicationStatus** (str enum):
`Applied`, `Interviewing`, `Offer`, `Accepted`, `Rejected`, `Ghosted`

**InterviewType** (str enum):
`Phone Screen`, `HR Interview`, `Technical`, `System Design`, `Behavioral`, `Take-home`, `Final Round`, `Culture Fit`, `Other`

**Application** (sqlmodel table):
| Field | Type | Required | Notes |
|---|---|---|---|
| id | int (PK, auto) | auto | |
| position | str | yes | |
| company | str | yes | |
| status | ApplicationStatus | yes | default: Applied |
| cv | str | no | |
| applied_date | date | no | ISO 8601 (YYYY-MM-DD) |
| location | str | no | |
| salary | str | no | |
| applied_through | str | no | |
| notes | str | no | |
| created_at | datetime | auto | |

**Interview** (sqlmodel table):
| Field | Type | Required | Notes |
|---|---|---|---|
| id | int (PK, auto) | auto | |
| application_id | int (FK) | yes | cascading delete |
| date | date | yes | ISO 8601 (YYYY-MM-DD) |
| time | str | yes | HH:MM (24h) |
| type | InterviewType | yes | |
| notes | str | no | |
| interviewer | str | no | |

### Status State Machine

```
Applied ──► Interviewing ──► Offer ──► Accepted
   │              │             │
   ├──► Rejected ◄──┴──► Ghosted ◄──┘
```

Rules:
- Forward progression: Applied → Interviewing → Offer → Accepted
- Rejection allowed from any active status (Applied, Interviewing, Offer)
- Ghosted allowed from any active status (Applied, Interviewing, Offer)
- Terminal statuses (Accepted, Rejected, Ghosted) cannot transition further
- Self-transitions (same status) are allowed

### API Endpoints

| Method | Path | Status | Description |
|---|---|---|---|
| GET | /health | 200 | Health check |
| POST | /test/reset | 200 | Reset database (test only) |
| POST | /applications | 201 | Create application |
| GET | /applications | 200 | List (filter: ?status, ?company, ?location) |
| GET | /applications/{id} | 200/404 | Get by ID |
| PATCH | /applications/{id} | 200/404 | Partial update |
| DELETE | /applications/{id} | 204/404 | Delete (cascade interviews) |
| GET | /applications/summary | 200 | Status count summary |
| POST | /applications/{id}/interviews | 201/404 | Create interview |
| GET | /applications/{id}/interviews | 200/404 | List for application |
| GET | /applications/{id}/interviews/{iid} | 200/404 | Get by ID |
| PATCH | /applications/{id}/interviews/{iid} | 200/404 | Partial update |
| DELETE | /applications/{id}/interviews/{iid} | 204/404 | Delete |

### Validation

- `position`, `company`: required, non-empty strings (min 1 char)
- `status`: must be a valid ApplicationStatus enum value
- `applied_date`: must be valid ISO date (YYYY-MM-DD)
- `date` (interview): must be valid ISO date (YYYY-MM-DD)
- `time` (interview): must be HH:MM 24h format
- `type` (interview): must be valid InterviewType enum value
- 422 with `detail` array for validation errors matching FastAPI/pydantic format
- 404 with `{"detail": "Application not found"}` or `{"detail": "Interview not found"}`

### Error Responses

- Validation errors: 422 with FastAPI's standard validation error format
- Not found: 404 with `{"detail": "<resource> not found"}`
