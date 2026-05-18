from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.database import get_session
from app.models.interview import InterviewCreate, InterviewPublic, InterviewUpdate
from app.services import interview_service

router = APIRouter()


@router.post("/applications/{application_id}/interviews", status_code=status.HTTP_201_CREATED)
def create_interview(
    application_id: int,
    body: InterviewCreate,
    session: Session = Depends(get_session),
) -> InterviewPublic:
    return interview_service.create(session, application_id, body.model_dump())


@router.get("/applications/{application_id}/interviews")
def list_interviews(
    application_id: int,
    session: Session = Depends(get_session),
) -> list[InterviewPublic]:
    return interview_service.list_for_application(session, application_id)


@router.get("/applications/{application_id}/interviews/{interview_id}")
def get_interview(
    application_id: int,
    interview_id: int,
    session: Session = Depends(get_session),
) -> InterviewPublic:
    return interview_service.get_by_id(session, application_id, interview_id)


@router.patch("/applications/{application_id}/interviews/{interview_id}")
def update_interview(
    application_id: int,
    interview_id: int,
    body: InterviewUpdate,
    session: Session = Depends(get_session),
) -> InterviewPublic:
    return interview_service.update(
        session, application_id, interview_id, body.model_dump(exclude_none=True)
    )


@router.delete(
    "/applications/{application_id}/interviews/{interview_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_interview(
    application_id: int,
    interview_id: int,
    session: Session = Depends(get_session),
):
    interview_service.delete(session, application_id, interview_id)
