from typing import Optional

from pydantic import BaseModel

class ExerciseReq(BaseModel):
    exercise_id: str
    sets: int
    reps: int
    weight: float | int

class WorkoutReq(BaseModel):
    username: str
    name: str

class EditExercise(BaseModel):
    exercise_id: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float | int] = None