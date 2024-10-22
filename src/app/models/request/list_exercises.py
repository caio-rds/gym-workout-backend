from typing import Optional
from pydantic import BaseModel

class NewExercise(BaseModel):
    name: str
    muscle_group: str
    equipment: str | list[str]
    description: str

class EditExercise(BaseModel):
    id: str
    name: Optional[str] = None
    muscle_group: Optional[str] = None
    equipment: Optional[str | list[str]] = None
    description: Optional[str] = None