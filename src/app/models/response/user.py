from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    email: str
    name: str
    phone: str
    activity_level: float
    bmi: float | int
    bmr: float | int
    tdee: float | int
    weight: float | int
    height: int
    birth_date: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None