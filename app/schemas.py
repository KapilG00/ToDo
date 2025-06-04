from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoCreate(BaseModel):
    title: str = ""
    description: str = ""
    completed: bool = False


class TodoRead(TodoCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoUpdate(TodoCreate):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
