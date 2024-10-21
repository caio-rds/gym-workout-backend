from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from src.app.controllers.exercises import add_exercise, delete_exercise, read_exercise, update_exercise
from src.app.models.request.exercises import ExerciseReq, EditExercise

router = APIRouter()

@router.get('/{workout_id}')
async def handler_get_exercise(workout_id: str):
    return await read_exercise(workout_id)

@router.post('/{workout_id}')
async def handler_new_exercise(workout_id: str, exercise: ExerciseReq | list[ExerciseReq]):
    if isinstance(exercise, list):
        result = []
        for ex in exercise:
            result.append(await add_exercise(workout_id, ex))
        return jsonable_encoder({"exercises": result})
    return await add_exercise(workout_id, exercise)

@router.put('/{exercise_id}')
async def handler_edit_exercise(exercise_id: str, exercise: EditExercise):
    return await update_exercise(exercise_id, exercise)

@router.delete('/{exercise_id}')
async def handler_delete_exercise(exercise_id: str):
    return await delete_exercise(exercise_id)