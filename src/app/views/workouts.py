from fastapi import APIRouter, Depends
from src.app.controllers.workouts import create_workout, read_workouts, read_workout, delete_workout, edit_workout
from src.app.models.request.exercises import WorkoutReq
from src.app.utils.auth import auth_wrapper

router = APIRouter()

@router.get("/")
async def handler_read_workouts(_id: str = None, username=Depends(auth_wrapper)):
    if username:
        if not _id:
            return await read_workouts(username)
        return await read_workout(_id)

@router.post('/')
async def handler_create_workout(workout: WorkoutReq, username=Depends(auth_wrapper)):
    if username:
        return await create_workout(workout)

@router.put('/{workout_id}')
async def handler_edit_workout(workout_id: str, new_name: str, username=Depends(auth_wrapper)):
    if username:
        return await edit_workout(workout_id, new_name)

@router.delete('/{workout_id}')
async def handler_delete_workout(workout_id: str, username = Depends(auth_wrapper)):
    if username:
        return await delete_workout(workout_id)