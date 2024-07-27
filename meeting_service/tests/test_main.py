import pytest


@pytest.mark.asyncio
async def test_read_main(test_client):
    client, db_session = test_client

    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Meeting Service API"}
