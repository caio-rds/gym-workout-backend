import datetime
from src.app.models.request.exercises import ExerciseReq, EditExercise
from src.app.schemas.workouts import Workout, ExerciseList, Exercise
from src.app.utils.custom_exceptions import NotFound, ExerciseNotFound, WorkoutNotFound

async def read_exercise(workout_id: str) -> Exercise:
    exercises = await Exercise.get(workout_id)
    if not exercises:
        raise ExerciseNotFound
    return exercises

async def add_exercise(workout_id: str, exercise: ExerciseReq):
    user_workout = await Workout.get(workout_id)
    if not user_workout:
        raise WorkoutNotFound(workout_id)
    exercise_in_db = await ExerciseList.get(exercise.exercise_id)
    if not exercise_in_db:
        raise ExerciseNotFound(exercise.exercise_id)

    inserted = await Exercise(
        name=exercise_in_db.name,
        muscle_group=exercise_in_db.muscle_group,
        equipment=exercise_in_db.equipment,
        description=exercise_in_db.description,
        sets=exercise.sets,
        reps=exercise.reps,
        weight=exercise.weight,
        workout_id=workout_id
    ).insert()
    return inserted

async def update_exercise(exercise_id: str, exercise: EditExercise):
    current_exercise = await Exercise.get(exercise_id)
    if not current_exercise:
        raise ExerciseNotFound
    if exercise.exercise_id:
        exercise_in_db = await ExerciseList.get(exercise.exercise_id)
        if not exercise_in_db:
            raise NotFound("Exercise to change not found")
        current_exercise.name = exercise_in_db.name
        current_exercise.muscle_group = exercise_in_db.muscle_group
        current_exercise.equipment = exercise_in_db.equipment
        current_exercise.description = exercise_in_db.description
    if exercise.sets:
        current_exercise.sets = exercise.sets
    if exercise.reps:
        current_exercise.reps = exercise.reps
    if exercise.weight:
        current_exercise.weight = exercise.weight
    current_exercise.updated_at = datetime.datetime.now().isoformat()
    await current_exercise.save()
    return current_exercise

async def delete_exercise(exercise_id: str):
    exercise = await Exercise.get(exercise_id)
    if not exercise:
        raise ExerciseNotFound
    await exercise.delete()
    return exercise