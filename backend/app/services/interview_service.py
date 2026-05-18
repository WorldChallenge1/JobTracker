from fastapi import HTTPException
from sqlmodel import Session

from app.models.interview import Interview
from app.repositories import application_repository, interview_repository


def _require_application(session: Session, application_id: int):
    application = application_repository.get_by_id(session, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")


def create(session: Session, application_id: int, data: dict) -> Interview:
    _require_application(session, application_id)
    data["application_id"] = application_id
    return interview_repository.create(session, data)


def get_by_id(session: Session, application_id: int, id: int) -> Interview:
    _require_application(session, application_id)
    interview = interview_repository.get_by_id(session, id)
    if not interview or interview.application_id != application_id:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


def list_for_application(session: Session, application_id: int) -> list[Interview]:
    _require_application(session, application_id)
    return interview_repository.list_for_application(session, application_id)


def update(session: Session, application_id: int, id: int, data: dict) -> Interview:
    _require_application(session, application_id)
    interview = interview_repository.get_by_id(session, id)
    if not interview or interview.application_id != application_id:
        raise HTTPException(status_code=404, detail="Interview not found")
    result = interview_repository.update(session, id, data)
    assert result is not None
    return result


def delete(session: Session, application_id: int, id: int):
    _require_application(session, application_id)
    interview = interview_repository.get_by_id(session, id)
    if not interview or interview.application_id != application_id:
        raise HTTPException(status_code=404, detail="Interview not found")
    interview_repository.delete(session, id)
