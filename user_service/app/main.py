from app.routers import user
from fastapi import FastAPI

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "User Service"}
