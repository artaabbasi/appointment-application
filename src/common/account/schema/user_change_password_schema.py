from pydantic import BaseModel


class UserChangePasswordSchema(BaseModel):
    code: str
    password: str
    password_repeated: str
