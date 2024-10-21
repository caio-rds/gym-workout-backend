from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from src.app.schemas.workouts import Workout, ExerciseList, Exercise
from src.app.schemas.login import TryLogin
from src.app.schemas.user import CreateUser, ReadUser, UpdatedUser
from src.app.views.workouts import router as workout_router
from src.app.views.exercises import router as exercises_router
from src.app.views.user import router as user_router
from src.app.views.login import router as login_router
import logging
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

@asynccontextmanager
async def lifespan(app_: FastAPI):
    client = AsyncIOMotorClient(os.getenv('DATABASE_URL'))
    await init_beanie(
        database=client.get_database('gym'),
        document_models=[
            CreateUser,ReadUser, UpdatedUser, TryLogin, Workout, ExerciseList, Exercise
        ]
    )
    logging.info('Beanie initialized with MongoDB')
    app_.include_router(workout_router, prefix='/workouts', tags=['workouts'])
    app_.include_router(exercises_router, prefix='/workouts/exercises', tags=['exercises'])
    app_.include_router(user_router, prefix='/user', tags=['users'])
    app_.include_router(login_router, prefix='/login', tags=['login'])
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)