import os

from sqlmodel import SQLModel, Session, create_engine

sqlite_url = os.getenv("DATABASE_URL", "sqlite:///./jobtracker.db")
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
