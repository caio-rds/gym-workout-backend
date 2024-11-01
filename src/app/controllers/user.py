import datetime

from pymongo.errors import DuplicateKeyError
from src.app.models.response.user import UserResponse
from src.app.schemas.user import User
from src.app.models.request.user import UpdateUser, UserDeleted, CreateUser
from src.app.utils.auth import pwd_hash
from src.app.utils.custom_exceptions import UserNotFound, UserAlreadyExists


async def create(new_user: CreateUser) -> UserResponse:
    try:
        new_user.password = await pwd_hash(new_user.password)
        user = User(**new_user.model_dump(exclude_none=True))
        user.bmr = await calculate_bmr(user.weight, user.height, user.birth_date, user.gender)
        user.tdee = await calculate_tdee(user.bmr, user.activity_level)
        user.bmi = await calculate_bmi(user.weight, user.height)
        user.created_at = datetime.datetime.now(datetime.UTC)
        await user.insert()
        return UserResponse(**user.model_dump(exclude_none=True))
    except DuplicateKeyError as e:
        raise UserAlreadyExists(e.details.get('keyValue'))

async def read(identifier: str, find_by: str = 'username') -> UserResponse:
    queries = {
        'username': User.username == identifier,
        'email': User.email == identifier.replace('%40', '@')
    }
    if user := await User.find_one(queries.get(find_by)):
        return UserResponse(**user.model_dump(exclude_none=True))
    raise UserNotFound

async def update(user_update: UpdateUser) -> UserResponse:
    if user := await User.find_one(User.username == user_update.username):
        for key, value in user_update.model_dump(exclude_unset=True).items():
            if key == 'password':
                value = await pwd_hash(value)
            setattr(user, key, value)
        user.bmr = await calculate_bmr(user.weight, user.height, user.birth_date, user.gender)
        user.tdee = await calculate_tdee(user.bmr, user.activity_level)
        user.bmi = await calculate_bmi(user.weight, user.height)
        user.updated_at = datetime.datetime.now(datetime.UTC)
        await user.save()
        return UserResponse(**user.model_dump(exclude_none=True))
    raise UserNotFound

async def delete(username: str):
    if user := await User.find_one(User.username == username):
        await user.delete()
        return UserDeleted(
            username=user.username,
            message='User deleted successfully',
            status=True,
            id=str(user.id)
        )
    raise UserNotFound


async def calculate_bmr(weight: float or int, height: int, birth_date: str, gender: str) -> float:
    age = datetime.datetime.now().year - int(birth_date.split('/')[2])
    if gender.lower() == 'male':
        return round(66 + (13.75 * weight) + (5 * height) - (6.75 * age), 2)
    elif gender.lower() == 'female':
        return round(655 + (9.56 * weight) + (1.85 * height) - (4.68 * age), 2)
    else:
        raise ValueError("Gender must be 'male' or 'female'")

async def calculate_tdee(bmr: float or int, activity_level: float) -> float:
    return round(bmr * activity_level, 2)

async def calculate_bmi(weight: float or int, height: int) -> float:
    return round((weight / (height / 100) ** 2), 2)