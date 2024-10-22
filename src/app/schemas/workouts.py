from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from beanie import Document, Indexed
from bson import ObjectId

class Exercise(Document):
    name: str
    muscle_group: str
    equipment: str | list[str]
    description: str
    sets: int
    reps: int
    weight: float | int
    exercise_id: Indexed(str)
    workout_id: Indexed(str)
    created_at: Optional[str] = datetime.now().isoformat()
    updated_at: Optional[str] = None

    class Settings:
        name = 'exercises'


class Workout(Document):
    _id: ObjectId
    username: Indexed(str)
    name: str
    created_at: Optional[str] = datetime.now().isoformat()
    updated_at: Optional[str] = None

    class Settings:
        name = 'workout'

class WorkoutRead(Document):
    _id: ObjectId
    username: Indexed(str)
    name: str
    created_at: Optional[str] = datetime.now().isoformat()
    updated_at: Optional[str] = None

    class Settings:
        name = 'workout'


class ExerciseList(Document):
    _id: ObjectId
    name: str
    muscle_group: str
    equipment: str | list[str]
    description: str

    class Settings:
        name = 'exercise_list'