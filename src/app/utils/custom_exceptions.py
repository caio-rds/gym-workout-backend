from fastapi import HTTPException


class NotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        raise HTTPException(status_code=404, detail=self.message)


class GenericException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
        raise HTTPException(status_code=self.status_code, detail=self.message)


class InvalidID(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        raise HTTPException(status_code=400, detail=self.message)


class PasswordMismatch(GenericException):
    def __init__(self):
        super().__init__('Password does not match', 400)


class UserNotFound(GenericException):
    def __init__(self):
        super().__init__('User not found', 404)

class UserAlreadyExists(GenericException):
    def __init__(self, message: dict):
        if message.get('username'):
            super().__init__(f"Username already in use: {message.get('username')}", 400)
        if message.get('email'):
            super().__init__(f"Email already in use: {message.get('email')}", 400)


class CodeNotFound(GenericException):
    def __init__(self):
        super().__init__('Code not found', 404)


class ExerciseNotFound(Exception):
    def __init__(self, _id: str):
        self.message = f'Exercise with id {_id} not found'
        super().__init__(self.message)
        raise HTTPException(status_code=404, detail=self.message)

class WorkoutNotFound(Exception):
    def __init__(self, _id: str):
        self.message = f'Workout with id {_id} not found'
        super().__init__(self.message)
        raise HTTPException(status_code=404, detail=self.message)


class InvalidToken(GenericException):
    def __init__(self):
        super().__init__('Invalid token', 401)


class TokenExpired(GenericException):
    def __init__(self):
        super().__init__('Token expired', 401)


class InvalidTokenSignature(GenericException):
    def __init__(self):
        super().__init__('Invalid token signature', 401)


class BearerNotFound(GenericException):
    def __init__(self):
        super().__init__('Bearer token not found', 401)

class InvalidPhoneFormat(GenericException):
    def __init__(self):
        super().__init__('Invalid phone number format', 400)

class InvalidEmailFormat(GenericException):
    def __init__(self):
        super().__init__('Invalid email format', 400)

class InvalidName(GenericException):
    def __init__(self):
        super().__init__('Invalid full name format', 400)

class InvalidWeight(GenericException):
    def __init__(self):
        super().__init__('Weight must be greater than 0', 400)

class InvalidHeight(GenericException):
    def __init__(self):
        super().__init__('Height must be greater than 0', 400)

class InvalidBirthDate(GenericException):
    def __init__(self):
        super().__init__('Birth date must be less than today', 400)

class InvalidDateFormat(GenericException):
    def __init__(self):
        super().__init__('Invalid date format', 400)