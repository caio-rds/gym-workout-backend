from fastapi import APIRouter

from src.app.controllers.list_exercises import create, read, update, delete
from src.app.models.request.list_exercises import NewExercise, EditExercise

router = APIRouter()

@router.post('/')
async def create_exercise(payload: NewExercise):
    return await create(payload)

@router.get('/{exercise_id}')
async def get_exercise(exercise_id: str):
    if exercise_id == 'all':
        return await read(None)
    return await read(exercise_id)

@router.put('/')
async def update_exercise(payload: EditExercise):
    return await update(payload)

@router.delete('/{exercise_id}')
async def delete_exercise(exercise_id: str):
    return await delete(exercise_id)