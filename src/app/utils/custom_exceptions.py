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
    def __init__(self):
        super().__init__('User already exists', 409)


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