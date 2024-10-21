# GYM WORKOUT BACKEND

## Simple backend for a gym workout app.
 
Here is information about the project.
- Language/Framework: **Python** *3.12* / **FastAPI**
- Pattern used: **MVC**
- Database: **MongoDB** with *Beanie ODM*
- Authentication: JWT
- Tests: Pytest
- Dockerized

## Installation

1. Clone the repository
2. Install the dependencies
3. Run the server

```bash
git clone
cd gym-workout-backend
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Run in Docker

1. Build the image
2. Run the container

```bash
docker build -t gym-workout-backend .
docker run -d -p 8000:8000 gym-workout-backend
```

## Usage

- Create a user
- Login
- Create a workout
- Create exercises for the workout
- Create sets for the exercises
- Get the workout with exercises and sets
- Update the workout
- Delete the workout

