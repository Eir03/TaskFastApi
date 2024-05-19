from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., example="Купить пачку чипсОв")
    description: Optional[str] = Field(None, example="С крабом лейс")

class TaskCreate(TaskBase):
    completed: bool = Field(default=False, example=False)

class TaskUpdate(TaskBase):
    title: Optional[str] = Field(None, example="Приготовить ленивые голубцы")
    description: Optional[str] = Field(None, example="Но ленивый только ты")
    completed: Optional[bool] = Field(None, example=False)

class TaskStatusUpdate(BaseModel):
    completed: bool

class TaskSchema(TaskBase):
    id: int
    completed: bool

    class Config:
        from_attributes = True
