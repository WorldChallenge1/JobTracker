from fastapi import APIRouter
from sqlmodel import SQLModel

from app.database import engine

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/test/reset")
def reset_database():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    return {"status": "reset"}
