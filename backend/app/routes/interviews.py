from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.database import get_session
from app.models.interview import InterviewCreate, InterviewPublic, InterviewUpdate
from app.services import interview_service

router = APIRouter()


@router.post(
    "/applications/{application_id}/interviews", status_code=status.HTTP_201_CREATED
)
def create_interview(
    application_id: int,
    body: InterviewCreate,
    session: Session = Depends(get_session),
) -> InterviewPublic:
    created = interview_service.create(session, application_id, body.model_dump())
    return InterviewPublic.model_validate(created)


@router.get("/applications/{application_id}/interviews")
def list_interviews(
    application_id: int,
    session: Session = Depends(get_session),
) -> list[InterviewPublic]:
    interview_list = interview_service.list_for_application(session, application_id)
    return [InterviewPublic.model_validate(interview) for interview in interview_list]


@router.get("/applications/{application_id}/interviews/{interview_id}")
def get_interview(
    application_id: int,
    interview_id: int,
    session: Session = Depends(get_session),
) -> InterviewPublic:
    found_interview = interview_service.get_by_id(session, application_id, interview_id)
    return InterviewPublic.model_validate(found_interview)


@router.patch("/applications/{application_id}/interviews/{interview_id}")
def update_interview(
    application_id: int,
    interview_id: int,
    body: InterviewUpdate,
    session: Session = Depends(get_session),
) -> InterviewPublic:
    updated_interview = interview_service.update(
        session, application_id, interview_id, body.model_dump(exclude_none=True)
    )
    return InterviewPublic.model_validate(updated_interview)


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
