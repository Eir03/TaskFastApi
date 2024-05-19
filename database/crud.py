from sqlalchemy.orm import Session
from .base import Task  # SQLAlchemy модель
from schemas.task import TaskCreate, TaskUpdate, TaskSchema  # Pydantic модели
from typing import List

def create_task(db: Session, task_data: TaskCreate):
    # Создаем экземпляр модели Task, используя данные из Pydantic модели
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, skip: int = 0, limit: int = 10) -> List[TaskSchema]:
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return [TaskSchema.from_orm(task) for task in tasks]  # Сериализация через Pydantic модели

def get_task(db: Session, task_id: int) -> TaskSchema:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        return TaskSchema.from_orm(task)
    return None  # Возвращаем None, если задача не найдена

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    # Получаем задачу по ID
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        # Обновляем поля задачи данными из Pydantic модели
        task.title = task_data.title if task_data.title is not None else task.title
        task.description = task_data.description if task_data.description is not None else task.description
        task.completed = task_data.completed if task_data.completed is not None else task.completed
        db.commit()
        db.refresh(task)
        return task
    return None

def update_task_status(db: Session, task_id: int, new_status: bool):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completed = new_status
        db.commit()
        db.refresh(task)
        return task
    return None

def delete_task(db: Session, task_id: int) -> bool:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False
