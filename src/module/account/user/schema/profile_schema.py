from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    phone_number: str
    fullname: str
