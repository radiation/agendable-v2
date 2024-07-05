from contextlib import asynccontextmanager

import databases
import sqlalchemy
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from routers import user

DATABASE_URL = "postgresql://user:password@postgres:5432/user_db"

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

app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "User Service"}
