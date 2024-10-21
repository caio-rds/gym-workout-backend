from fastapi.encoders import jsonable_encoder

from src.app.schemas.login import TryLogin
from src.app.utils.auth import check_pwd, encode_token
from src.app.utils.custom_exceptions import PasswordMismatch, UserNotFound


async def match_user(username: str, password: str, login_ip: str, user_agent: str) -> dict:
    if user := await TryLogin.find_one(TryLogin.username == username):
        if await check_pwd(password, user.password):
            return jsonable_encoder({
                'token': await encode_token(username)
            })
        raise PasswordMismatch
    raise UserNotFound
