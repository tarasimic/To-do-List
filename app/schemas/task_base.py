from pydantic import BaseModel
from datetime import date

class TaskBase(BaseModel):

    name: str
    description: str
    due_date: date

class DeleteTask(BaseModel):
    id: int