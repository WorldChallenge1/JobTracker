from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.database import get_session
from app.models.application import (
    ApplicationCreate,
    ApplicationPublic,
    ApplicationStatus,
    ApplicationUpdate,
)
from app.services import application_service

router = APIRouter()


@router.post("/applications", status_code=status.HTTP_201_CREATED)
def create_application(
    body: ApplicationCreate,
    session: Session = Depends(get_session),
) -> ApplicationPublic:
    return application_service.create(session, body.model_dump())


@router.get("/applications")
def list_applications(
    status: Optional[ApplicationStatus] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    session: Session = Depends(get_session),
) -> list[ApplicationPublic]:
    return application_service.list_all(session, status, company, location)


@router.get("/applications/summary")
def get_summary(
    session: Session = Depends(get_session),
) -> list[dict]:
    return application_service.get_status_summary(session)


@router.get("/applications/{id}")
def get_application(
    id: int,
    session: Session = Depends(get_session),
) -> ApplicationPublic:
    return application_service.get_by_id(session, id)


@router.patch("/applications/{id}")
def update_application(
    id: int,
    body: ApplicationUpdate,
    session: Session = Depends(get_session),
) -> ApplicationPublic:
    return application_service.update(session, id, body.model_dump(exclude_none=True))


@router.delete("/applications/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    id: int,
    session: Session = Depends(get_session),
):
    application_service.delete(session, id)
