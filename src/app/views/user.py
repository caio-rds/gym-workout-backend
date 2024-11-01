from fastapi import APIRouter, HTTPException

from src.app.controllers.user import create, read, update, delete
from src.app.models.request.user import UpdateUser, CreateUser
from src.app.models.response.user import UserResponse
from src.app.schemas.user import User

router = APIRouter()


@router.post('/', response_model=UserResponse, response_model_exclude_unset=True)
async def create_user(new_user: CreateUser) -> UserResponse:
    return await create(new_user)


@router.get('/{identifier}', response_model=UserResponse, response_model_exclude_unset=True)
async def get_user(identifier: str, find_by: str = 'username') -> UserResponse:
    if find_by not in ['username', 'email']:
        raise HTTPException(
            status_code=400,
            detail='Invalid parameter find_by, must be username(default) or email'
        )
    return await read(identifier, find_by)


@router.put('/', response_model=UserResponse, response_model_exclude_unset=True)
async def update_user(user: UpdateUser) -> UserResponse:
    return await update(user)


@router.delete('/{username}')
async def delete_user(username: str):
    return await delete(username)

