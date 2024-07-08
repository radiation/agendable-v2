from contextlib import asynccontextmanager

import databases
import sqlalchemy
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from routers import meeting, meeting_attendees, meeting_tasks, tasks

DATABASE_URL = "postgresql://user:password@postgres:5432/meeting_db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()

    # Run Alembic migrations
    alembic_cfg = Config("/migrations/alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield

    # Shutdown
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(meeting.router)
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(
    meeting_tasks.router, prefix="/meeting_tasks", tags=["meeting_tasks"]
)
app.include_router(
    meeting_attendees.router, prefix="/meeting_attendees", tags=["meeting_attendees"]
)


@app.get("/")
async def root():
    return {"message": "Meeting Service"}
