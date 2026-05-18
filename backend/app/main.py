from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import applications, interviews, test


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(test.router)
app.include_router(applications.router)
app.include_router(interviews.router)
