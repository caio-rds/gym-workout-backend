import datetime

from beanie import Document, Indexed
import re
from src.app.utils.validations import validate_password
from fastapi import HTTPException
import bson

class CreateUser(Document):
    username: Indexed(str, unique=True)
    email: Indexed(str, unique=True)
    password: str
    name: str
    phone: str

    def __init__(self, **data):
        super().__init__(**data)
        try:
            validate_password(self.password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        if re.search(r"\(\d{2}\)\s+\d{5}-\d{4}", self.phone) is None:
            raise HTTPException(status_code=400, detail="Invalid phone number format")
        if re.search(r'^[a-z0-9]+[._]?[a-z0-9]+@\w+[.]\w{2,3}$', self.email) is None:
            raise HTTPException(status_code=400, detail="Invalid email format")
        if re.search(r"^[A-Za-záàâãéèêíìóòôõúùûüçÇ\-\s]+$", self.name) is None:
            raise HTTPException(status_code=400, detail="Invalid full name format")

    class Settings:
        name = "user"

class ReadUser(Document):
    _id: bson.ObjectId
    username: str
    email: str
    name: str
    phone: str

    class Settings:
        name = "user"

    @property
    def id(self):
        return self._id


class UpdatedUser(Document):
    username: str
    email: str
    name: str
    phone: str
    updated_at: datetime.datetime

    class Settings:
        name = "user"