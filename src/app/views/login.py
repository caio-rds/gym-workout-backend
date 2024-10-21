from http.client import HTTPException
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from src.app.controllers.login import match_user
from src.app.utils.auth import auth_wrapper

router = APIRouter()

@router.get("/")
async def login(username=Depends(auth_wrapper)) -> dict:
    if username:
        return {"username": username}
    raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/")
async def try_login(request: Request, form: OAuth2PasswordRequestForm = Depends()) -> dict:
    if user := await match_user(form.username, form.password, request.client.host, request.headers.get('User-Agent')):
        return user