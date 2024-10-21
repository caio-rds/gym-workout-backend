import datetime

from src.app.models.request.exercises import WorkoutReq
from src.app.models.response.workouts import WorkoutResponse
from src.app.schemas.workouts import Workout, Exercise
from src.app.utils.custom_exceptions import WorkoutNotFound
from src.app.utils.validations import to_bson

async def read_workouts(username: str) -> list[WorkoutResponse]:
    workouts = await Workout.aggregate(
        [
            {'$match': {'username': username}},
            {'$lookup': {
                'from': 'exercises',
                'let': {'workoutId': {'$toString': '$_id'}},
                'pipeline': [
                    {'$match': {'$expr': {'$eq': ['$workout_id', '$$workoutId']}}}
                ],
                'as': 'exercises'
            }}
        ]
    ).to_list(1000)
    if not workouts:
        raise WorkoutNotFound
    for workout in workouts:
        workout['_id'] = str(workout['_id'])
        for exercise in workout['exercises']:
            exercise['_id'] = str(exercise['_id'])

    return workouts

async def read_workout(workout_id: str) -> WorkoutResponse:
    workout = await Workout.aggregate(
        [
            {'$match': {'_id': await to_bson(workout_id)}},
            {'$lookup': {
                'from': 'exercises',
                'let': {'workoutId': {'$toString': '$_id'}},
                'pipeline': [
                    {'$match': {'$expr': {'$eq': ['$workout_id', '$$workoutId']}}}
                ],
                'as': 'exercises'
            }}
        ]
    ).to_list(1)
    if not workout:
        raise WorkoutNotFound
    workout = workout[0]
    workout['_id'] = str(workout['_id'])
    for exercise in workout['exercises']:
        exercise['_id'] = str(exercise['_id'])
    return workout

async def create_workout(workout: WorkoutReq):
    data = Workout(
        username=workout.username,
        name=workout.name
    )
    await data.insert()
    return data

async def edit_workout(workout_id: str, new_name: str):
    data = await Workout.get(workout_id)
    if not data:
        raise WorkoutNotFound
    data.name = new_name
    data.updated_at = datetime.datetime.now().isoformat()
    await data.save()
    return data

async def delete_workout(workout_id: str):
    workout = await Workout.get(workout_id)
    if not workout:
        raise WorkoutNotFound
    exercises = Exercise.find_many({'workout_id': workout_id})
    await exercises.delete()
    await workout.delete()
    return workout