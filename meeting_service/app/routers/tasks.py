from typing import List

import crud
import db
from fastapi import APIRouter, Depends
from schemas import task_schemas as schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks_by_user(user_id: int, db: Session = Depends(db.get_db)):
    return crud.get_tasks_by_user(db, user_id=user_id)


@router.post("/tasks/{task_id}/complete", status_code=200)
def complete_task(task_id: int, db: Session = Depends(db.get_db)):
    crud.mark_task_complete(db, task_id=task_id)
    return {"message": "Task marked as complete"}
