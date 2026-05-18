from typing import Optional

from fastapi import HTTPException
from sqlmodel import Session

from app.models.application import Application, ApplicationStatus
from app.repositories import application_repository

ALLOWED_TRANSITIONS: dict[ApplicationStatus, list[ApplicationStatus]] = {
    ApplicationStatus.Applied: [
        ApplicationStatus.Applied,
        ApplicationStatus.Interviewing,
        ApplicationStatus.Rejected,
        ApplicationStatus.Ghosted,
    ],
    ApplicationStatus.Interviewing: [
        ApplicationStatus.Interviewing,
        ApplicationStatus.Offer,
        ApplicationStatus.Rejected,
        ApplicationStatus.Ghosted,
    ],
    ApplicationStatus.Offer: [
        ApplicationStatus.Offer,
        ApplicationStatus.Accepted,
        ApplicationStatus.Rejected,
        ApplicationStatus.Ghosted,
    ],
    ApplicationStatus.Accepted: [ApplicationStatus.Accepted],
    ApplicationStatus.Rejected: [ApplicationStatus.Rejected],
    ApplicationStatus.Ghosted: [ApplicationStatus.Ghosted],
}


def _validate_status_transition(current: ApplicationStatus, new: ApplicationStatus):
    if new not in ALLOWED_TRANSITIONS.get(current, []):
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "type": "value_error",
                    "loc": ["body", "status"],
                    "msg": f"Invalid status transition from '{current.value}' to '{new.value}'",
                    "input": new.value,
                }
            ],
        )


def create(session: Session, data: dict) -> Application:
    return application_repository.create(session, data)


def get_by_id(session: Session, id: int) -> Application:
    application = application_repository.get_by_id(session, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


def list_all(
    session: Session,
    status: Optional[ApplicationStatus] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
) -> list[Application]:
    return application_repository.list_all(session, status, company, location)


def update(session: Session, id: int, data: dict) -> Application:
    application = application_repository.get_by_id(session, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if "status" in data and data["status"] is not None:
        _validate_status_transition(application.status, data["status"])
    return application_repository.update(session, id, data)


def delete(session: Session, id: int):
    if not application_repository.delete(session, id):
        raise HTTPException(status_code=404, detail="Application not found")


def get_status_summary(session: Session) -> list[dict]:
    return application_repository.get_status_summary(session)
