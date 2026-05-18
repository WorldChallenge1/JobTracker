from typing import Optional

from sqlmodel import Session, col, func, select

from app.models.application import Application, ApplicationStatus


def create(session: Session, data: dict) -> Application:
    application = Application(**data)
    session.add(application)
    session.commit()
    session.refresh(application)
    return application


def get_by_id(session: Session, id: int) -> Optional[Application]:
    return session.get(Application, id)


def list_all(
    session: Session,
    status: Optional[ApplicationStatus] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
) -> list[Application]:
    query = select(Application)
    if status:
        query = query.where(Application.status == status)
    if company:
        query = query.where(Application.company == company)
    if location:
        query = query.where(Application.location == location)
    return list(session.exec(query).all())


def update(session: Session, id: int, data: dict) -> Optional[Application]:
    application = session.get(Application, id)
    if not application:
        return None
    for key, value in data.items():
        if value is not None:
            setattr(application, key, value)
    session.add(application)
    session.commit()
    session.refresh(application)
    return application


def delete(session: Session, id: int) -> bool:
    application = session.get(Application, id)
    if not application:
        return False
    session.delete(application)
    session.commit()
    return True


def get_status_summary(session: Session) -> list[dict]:
    results = []
    for status in ApplicationStatus:
        count = session.exec(
            select(func.count(col(Application.id))).where(Application.status == status)
        ).one()
        results.append({"status": status.value, "count": count})
    return results
