import datetime
import os
from datetime import timedelta
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.app.utils.custom_exceptions import InvalidToken, TokenExpired, InvalidTokenSignature, GenericException, \
    BearerNotFound

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET")


async def pwd_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)


async def check_pwd(pwd: str, passwd_hash: str) -> bool:
    return pwd_context.verify(pwd, passwd_hash)


async def encode_token(username: str) -> str:
    payload = {
        "exp": datetime.datetime.now(datetime.UTC) + timedelta(hours=2),
        "iat": datetime.datetime.now(datetime.UTC),
        "sub": username
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


async def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        raise TokenExpired
    except jwt.InvalidTokenError:
        raise InvalidToken
    except jwt.InvalidSignatureError:
        raise InvalidTokenSignature
    except Exception as e:
        raise GenericException(str(e), 400)


async def auth_wrapper(token: str = Depends(oauth_scheme)) -> str:
    if token:
        return await decode_token(token)
    raise BearerNotFound


class AuthJWT:
    pass
