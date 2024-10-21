from bson import ObjectId
from bson.errors import InvalidId

from src.app.utils.custom_exceptions import InvalidID


def validate_password(password: str) -> bool:
    upper = False
    lower = False
    number = False
    special = False
    for char in password:
        if char.isupper():
            upper = True
        if char.islower():
            lower = True
        if char.isdigit():
            number = True
        if char in ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", ";",
                    ":", "'", '"', "<", ">", ",", ".", "?", "/"]:
            special = True
    if not upper:
        raise ValueError("Password must contain at least one uppercase letter")
    if not lower:
        raise ValueError("Password must contain at least one lowercase letter")
    if not number:
        raise ValueError("Password must contain at least one number")
    if not special:
        raise ValueError("Password must contain at least one special character")
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters")
    return True


async def to_bson(identifier: str) -> ObjectId:
    if isinstance(identifier, str):
        try:
            return ObjectId(identifier)
        except InvalidId:
            raise InvalidID(message=f'Invalid ID {identifier}')


async def validate_bson(identifier: str) -> bool:
    if not ObjectId.is_valid(identifier):
        raise InvalidID(message='Invalid ID')
    return True