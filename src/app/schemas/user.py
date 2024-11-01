import datetime
from typing import Optional
from beanie import Document, Indexed
import bson

class User(Document):
    _id: bson.ObjectId
    username: Indexed(str, unique=True)
    email: Indexed(str, unique=True)
    password: str
    name: str
    gender: str
    phone: str
    weight: float | int
    height: int
    birth_date: str
    activity_level: float
    bmr: float | int = None
    tdee: float | int = None
    bmi: float | int = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Settings:
        name = "user"