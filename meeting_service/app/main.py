from contextlib import asynccontextmanager

import databases
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from sqlalchemy import MetaData

from .routers import meeting

DATABASE_URL = "postgresql://user:password@postgres:5432/meeting_db"

database = databases.Database(DATABASE_URL)
metadata = MetaData()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()

    # Run Alembic migrations
    alembic_cfg = Config("app/alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield

    # Shutdown
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(meeting.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "User Service"}
