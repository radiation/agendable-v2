from app.db import get_db
from app.main import app
from app.models import Base
from config import settings
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_create_meeting():
    response = client.post(
        "/meetings/",
        json={
            "title": "Team Meeting",
            "start_date": "2023-01-01T09:00:00",
            "end_date": "2023-01-01T10:00:00",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Team Meeting"
    assert "id" in data
