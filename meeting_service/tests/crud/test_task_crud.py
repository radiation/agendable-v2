from datetime import datetime

import pytest
from app.crud.task_crud import create_task, delete_task, get_task, update_task
from app.schemas import task_schemas


async def create_test_task(db_session, title="Test Task"):
    task = task_schemas.TaskCreate(
        title=title,
        assignee_id=1,
        completed=False,
        due_date=datetime.now(),
    )
    task = await create_task(db_session, task)
    return task


@pytest.mark.asyncio
async def test_create_task(test_client):
    client, db_session = test_client

    new_task = task_schemas.TaskCreate(
        title="Test Task",
        assignee_id=1,
        completed=False,
        due_date=datetime.now(),
    )

    task = await create_task(db_session, new_task)
    assert task.title == "Test Task"

    # Refresh to get updated data
    await db_session.refresh(task)
    assert task.title == "Test Task"


@pytest.mark.asyncio
async def test_update_task(test_client):
    client, db_session = test_client

    task = await create_test_task(db_session, title="Initial Task")
    assert await get_task(db_session, task.id) is not None

    # Data to update
    update_data = task_schemas.TaskUpdate(title="Updated Task")
    updated_task = await update_task(db_session, task.id, update_data)
    assert updated_task.title == "Updated Task"

    # Refresh to get updated data
    await db_session.refresh(updated_task)
    assert updated_task.title == "Updated Task"


@pytest.mark.asyncio
async def test_delete_task(test_client):
    client, db_session = test_client

    task = await create_test_task(db_session, title="Task to Delete")
    assert await get_task(db_session, task.id) is not None

    # Delete the task
    await delete_task(db_session, task.id)

    # Ensure the task is deleted
    task = await get_task(db_session, task.id)
    assert task is None
