from typing import List

import crud.task_crud as crud
import db
from fastapi import APIRouter, Depends, HTTPException
from schemas import task_schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Create a new task
@router.post("/", response_model=task_schemas.Task)
async def create_task(
    task: task_schemas.TaskCreate, db: AsyncSession = Depends(db.get_db)
) -> task_schemas.Task:
    return await crud.create_task(db=db, task=task)


# List all tasks
@router.get("/", response_model=List[task_schemas.Task])
async def read_tasks(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> List[task_schemas.Task]:
    return await crud.get_tasks(db=db, skip=skip, limit=limit)


# Get a task by ID
@router.get("/{task_id}", response_model=task_schemas.Task)
async def read_task(
    task_id: int, db: AsyncSession = Depends(db.get_db)
) -> task_schemas.Task:
    task = await crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update an existing task
@router.put("/{task_id}", response_model=task_schemas.Task)
async def update_task(
    task_id: int,
    task: task_schemas.TaskUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> task_schemas.Task:
    updated_task = await crud.update_task(db=db, task_id=task_id, task=task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


# Delete a task
@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(db.get_db)):
    success = await crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")


# Get all tasks for a specific user
@router.get("/user/{user_id}", response_model=List[task_schemas.Task])
async def read_tasks_by_user(
    user_id: int, db: AsyncSession = Depends(db.get_db)
) -> List[task_schemas.Task]:
    return await crud.get_tasks_by_user(db=db, user_id=user_id)


# Mark a task as complete
@router.post("/{task_id}/complete", response_model=task_schemas.Task)
async def complete_task(
    task_id: int, db: AsyncSession = Depends(db.get_db)
) -> task_schemas.Task:
    task = await crud.mark_task_complete(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=404, detail="Task not found or already completed"
        )
    return task
