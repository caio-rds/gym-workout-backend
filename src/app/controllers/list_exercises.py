from src.app.models.request.list_exercises import NewExercise, EditExercise
from src.app.schemas.workouts import ExerciseList, Exercise
from src.app.utils.custom_exceptions import ExerciseNotFound


async def create(exercise: NewExercise):
    inserted = ExerciseList(**exercise.model_dump()).insert()
    return inserted

async def read(exercise_id: str | None = None):
    if exercise_id is None:
        return await ExerciseList.find_all().to_list()
    return await ExerciseList.get(exercise_id)

async def update(exercise: EditExercise):
    exercise_search = await ExerciseList.get(exercise.id)
    if exercise_search is None:
        raise ExerciseNotFound
    await exercise_search.update({"$set": exercise.model_dump(exclude_none=True, exclude={"id"})})
    exercises_in_workouts = Exercise.find({"exercise_id": exercise.id})
    await exercises_in_workouts.update({"$set": exercise.model_dump(exclude_none=True, exclude={"id"})})
    return exercise_search

async def delete(exercise_id: str):
    result = {
        'documents_deleted': 0,
        'exercise_id': None
    }
    exercise_in_db = await ExerciseList.get(exercise_id)
    if exercise_in_db is None:
        raise ExerciseNotFound
    exercises_in_workouts = Exercise.find({"exercise_id": exercise_id})
    deleted = await exercises_in_workouts.delete()
    result['documents_deleted'] += deleted.deleted_count
    result['exercise_id'] = exercise_id
    await exercise_in_db.delete()
    return result