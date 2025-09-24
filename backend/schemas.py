from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

class TaskCreate(BaseModel):
    user_id: int
    description: str

class TaskUpdate(BaseModel):
    completed:bool
    importance:int
