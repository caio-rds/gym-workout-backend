from fastapi import APIRouter, HTTPException

from src.app.controllers.user import create, read, update, delete
from src.app.models.request.user import RequestUpdateUser
from src.app.schemas.user import CreateUser, ReadUser, UpdatedUser

router = APIRouter()


@router.post('/', response_model=ReadUser, response_model_exclude_unset=True)
async def create_user(new_user: CreateUser) -> ReadUser:
    return await create(new_user)


@router.get('/{identifier}', response_model=ReadUser, response_model_exclude_unset=True)
async def get_user(identifier: str, find_by: str = 'id') -> ReadUser:
    params_values = ['id', 'username', 'email']
    if find_by not in params_values:
        raise HTTPException(
            status_code=400,
            detail='Invalid parameter find_by, must be id (default), username or email'
        )
    return await read(identifier, find_by)


@router.put('/', response_model=UpdatedUser, response_model_exclude_unset=True)
async def update_user(user: RequestUpdateUser) -> UpdatedUser:
    return await update(user)


@router.delete('/{username}')
async def delete_user(username: str):
    return await delete(username)

