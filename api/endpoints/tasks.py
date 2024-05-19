from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import crud
from database.session import get_db
from schemas.task import TaskSchema, TaskCreate, TaskUpdate, TaskStatusUpdate  # Используем Pydantic модели

router = APIRouter()

@router.get("/tasks/", response_model=List[TaskSchema], tags=["Задачи"])
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskSchema, tags=["Задачи"])
async def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@router.post("/tasks/", response_model=TaskSchema, tags=["Задачи"])
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    created_task = crud.create_task(db=db, task_data=task_data)  # Исправлено на task_data
    if not created_task:
        raise HTTPException(status_code=400, detail="Ошибка при создании задачи")
    return created_task

@router.put("/tasks/{task_id}", response_model=TaskSchema, tags=["Задачи"])
async def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db=db, task_id=task_id, task_data=task_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return updated_task

@router.patch("/tasks/{task_id}/status", response_model=TaskSchema, tags=["Задачи"])
async def update_task_status(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task_status(db=db, task_id=task_id, new_status=status_update.completed)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return updated_task

@router.delete("/tasks/{task_id}", tags=["Задачи"])
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    result = crud.delete_task(db=db, task_id=task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"message": "Удаление задачи успешно"}
