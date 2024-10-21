from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.schemas.user import ReadUser, CreateUser, UpdatedUser
from src.app.models.request.user import RequestUpdateUser, UserDeleted
from src.app.utils.auth import pwd_hash
from src.app.utils.custom_exceptions import UserNotFound, GenericException
from src.app.utils.validations import validate_bson


async def read(identifier: str, find_by: str = 'id') -> ReadUser:
    queries = {
        'username': ReadUser.username == identifier,
        'email': ReadUser.email == identifier.replace('%40', '@')
    }
    if find_by == 'id':
        if await validate_bson(identifier):
            queries['id'] = ReadUser.id == ObjectId(identifier)
    if user := await ReadUser.find_one(queries.get(find_by)):
        return user
    raise UserNotFound


async def create(new_user: CreateUser) -> ReadUser:
    try:
        new_user.password = await pwd_hash(new_user.password)
        user = await new_user.insert()
        return ReadUser(**user.model_dump())
    except DuplicateKeyError:
        raise GenericException(message='User already exists', status_code=400)


async def update(user_update: RequestUpdateUser) -> UpdatedUser:
    if user := await UpdatedUser.find_one(UpdatedUser.username == user_update.username):
        for key, value in user_update.model_dump(exclude_unset=True).items():
            if key == 'password':
                value = await pwd_hash(value)
            setattr(user, key, value)
        await user.save()
        return user
    raise UserNotFound


async def delete(username: str):
    if user := await ReadUser.find_one(ReadUser.username == username):
        await user.delete()
        return UserDeleted(
            username=user.username,
            message='User deleted successfully',
            status=True,
            id=str(user.id)
        )
    raise UserNotFound
