from beanie import Document


class TryLogin(Document):
    username: str
    password: str

    class Settings:
        name = 'user'