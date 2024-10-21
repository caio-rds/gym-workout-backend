from pydantic import BaseModel


class ExerciseResponse(BaseModel):
    _id: str
    name: str
    muscle_group: str
    equipment: str
    description: str
    sets: int
    reps: int
    weight: float | int
    workout_id: str
    created_at: str
    updated_at: str

class WorkoutResponse(BaseModel):
    _id: str
    username: str
    name: str
    exercises_muscle_groups: list[str]
    exercises: list[ExerciseResponse]
    created_at: str
    updated_at: str