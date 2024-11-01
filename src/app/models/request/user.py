import datetime
from typing import Optional
import re
from pydantic import BaseModel

from src.app.utils.custom_exceptions import (
    InvalidDateFormat, InvalidBirthDate, InvalidPhoneFormat, InvalidEmailFormat,
    InvalidName, InvalidWeight, InvalidHeight, GenericException)
from src.app.utils.validations import validate_password

patterns = {
    'phone': r"\(\d{2}\)\s+\d{5}-\d{4}",
    'email': r'^[a-z0-9]+[._]?[a-z0-9]+@\w+[.]\w{2,3}$',
    'name': r"^[A-Za-záàâãéèêíìóòôõúùûüçÇ\-\s]+$",
    'birth_date': r'^\d{2}/\d{2}/\d{4}$'
}

activity_levels = {
    1: 1.2,
    2: 1.375,
    3: 1.55,
    4: 1.725
}

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[float | int] = None
    birth_date: Optional[str] = None
    activity_level: Optional[int | float] = 1

    def __init__(self, **data):
        super().__init__(**data)
        if self.phone and re.search(patterns.get('phone'), self.phone) is None:
            raise InvalidPhoneFormat
        if self.email and re.search(patterns.get('email'), self.email) is None:
            raise InvalidEmailFormat
        if self.name and re.search(patterns.get('name'), self.name) is None:
            raise InvalidName
        if self.birth_date and re.search(patterns.get('birth_date'), self.birth_date) is None:
            raise InvalidDateFormat

        if self.weight and self.weight < 0:
            raise InvalidWeight

        if self.height and self.height < 0:
            raise InvalidHeight

        if self.birth_date:
            try:
                birth_date = datetime.datetime.strptime(str(self.birth_date), '%d/%m/%Y''').date()
            except ValueError:
                raise InvalidDateFormat
            if birth_date > datetime.date.today():
                raise InvalidBirthDate

        if self.activity_level:
            if self.activity_level not in activity_levels.keys():
                raise GenericException(message='Invalid activity level', status_code=400)
            self.activity_level = activity_levels.get(self.activity_level, None)
        if self.gender and self.gender not in ['Male', 'Female']:
            raise GenericException(message='Invalid Gender', status_code=400)


class CreateUser(UserBase):
    email: str
    password: str
    name: str
    phone: str
    weight: float | int
    height: int
    birth_date: str
    activity_level: int | float = 1

    def __init__(self, **data):
        super().__init__(**data)
        try:
            validate_password(self.password)
        except ValueError as e:
            raise GenericException(message=str(e), status_code=400)


class UpdateUser(UserBase):
    pass

class UserDeleted(BaseModel):
    status: bool
    message: str
    username: str
    id: str
