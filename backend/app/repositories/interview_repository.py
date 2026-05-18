from typing import Optional

from sqlmodel import Session, select

from app.models.interview import Interview


def create(session: Session, data: dict) -> Interview:
    interview = Interview(**data)
    session.add(interview)
    session.commit()
    session.refresh(interview)
    return interview


def get_by_id(session: Session, id: int) -> Optional[Interview]:
    return session.get(Interview, id)


def list_for_application(session: Session, application_id: int) -> list[Interview]:
    query = select(Interview).where(Interview.application_id == application_id)
    return list(session.exec(query).all())


def update(session: Session, id: int, data: dict) -> Optional[Interview]:
    interview = session.get(Interview, id)
    if not interview:
        return None
    for key, value in data.items():
        if value is not None:
            setattr(interview, key, value)
    session.add(interview)
    session.commit()
    session.refresh(interview)
    return interview


def delete(session: Session, id: int) -> bool:
    interview = session.get(Interview, id)
    if not interview:
        return False
    session.delete(interview)
    session.commit()
    return True
