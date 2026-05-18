import re
from datetime import date as date_type
from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.application import Application


class InterviewType(str, Enum):
    Phone_Screen = "Phone Screen"
    HR_Interview = "HR Interview"
    Technical = "Technical"
    System_Design = "System Design"
    Behavioral = "Behavioral"
    Take_home = "Take-home"
    Final_Round = "Final Round"
    Culture_Fit = "Culture Fit"
    Other = "Other"


_TIME_REGEX = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


class Interview(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id")
    date: date_type
    time: str
    type: InterviewType
    notes: Optional[str] = None
    interviewer: Optional[str] = None

    application: "Application" = Relationship(back_populates="interviews")


class InterviewCreate(SQLModel):
    date: date_type
    time: str
    type: InterviewType
    notes: Optional[str] = None
    interviewer: Optional[str] = None

    @field_validator("time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        if not _TIME_REGEX.match(v):
            raise ValueError("time must be in HH:MM format (24-hour)")
        return v


class InterviewUpdate(SQLModel):
    date: Optional[date_type] = None
    time: Optional[str] = None
    type: Optional[InterviewType] = None
    notes: Optional[str] = None
    interviewer: Optional[str] = None

    @field_validator("time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        if v is not None and not _TIME_REGEX.match(v):
            raise ValueError("time must be in HH:MM format (24-hour)")
        return v


class InterviewPublic(SQLModel):
    id: int
    application_id: int
    date: date_type
    time: str
    type: InterviewType
    notes: Optional[str] = None
    interviewer: Optional[str] = None
