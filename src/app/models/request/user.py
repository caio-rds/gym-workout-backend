import datetime
from typing import Optional

from fastapi import HTTPException
import re
from pydantic import BaseModel


class RequestUpdateUser(BaseModel):
    username: str
    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    updated_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)

    def __init__(self, **data):
        super().__init__(**data)
        if self.phone and re.search(r"\(\d{2}\)\s+\d{5}-\d{4}", self.phone) is None:
            raise HTTPException(status_code=400, detail="Invalid phone number format")
        if self.email and re.search(r'^[a-z0-9]+[._]?[a-z0-9]+@\w+[.]\w{2,3}$', self.email) is None:
            raise HTTPException(status_code=400, detail="Invalid email format")
        if self.full_name and re.search(r"^[A-Za-záàâãéèêíìóòôõúùûüçÇ\-\s]+$", self.name) is None:
            raise HTTPException(status_code=400, detail="Invalid full name format")


class UserDeleted(BaseModel):
    status: bool
    message: str
    username: str
    id: str
