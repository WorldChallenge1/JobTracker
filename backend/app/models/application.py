from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.interview import Interview


class ApplicationStatus(str, Enum):
    Applied = "Applied"
    Interviewing = "Interviewing"
    Offer = "Offer"
    Accepted = "Accepted"
    Rejected = "Rejected"
    Ghosted = "Ghosted"


class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    position: str
    company: str
    status: ApplicationStatus = Field(default=ApplicationStatus.Applied)
    cv: Optional[str] = None
    applied_date: Optional[date] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    applied_through: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    interviews: list["Interview"] = Relationship(
        back_populates="application", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class ApplicationCreate(SQLModel):
    position: str
    company: str
    status: ApplicationStatus = ApplicationStatus.Applied
    cv: Optional[str] = None
    applied_date: Optional[date] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    applied_through: Optional[str] = None
    notes: Optional[str] = None


class ApplicationUpdate(SQLModel):
    position: Optional[str] = None
    company: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    cv: Optional[str] = None
    applied_date: Optional[date] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    applied_through: Optional[str] = None
    notes: Optional[str] = None


class ApplicationPublic(SQLModel):
    id: int
    position: str
    company: str
    status: ApplicationStatus
    cv: Optional[str] = None
    applied_date: Optional[date] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    applied_through: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
